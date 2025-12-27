"""订单处理服务"""

from datetime import datetime
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.address import Address
from decimal import Decimal
import random
import string


class OrderService:
    """订单服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def generate_order_no(self) -> str:
        """生成订单号"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(random.choices(string.digits, k=6))
        return f"WO{timestamp}{random_str}"
    
    def create_order(self, user_id: int, address_id: int, items: list, remark: str = None) -> Order:
        """创建订单"""
        address = self.db.query(Address).filter(
            Address.id == address_id,
            Address.user_id == user_id
        ).first()
        if not address:
            raise Exception("地址不存在或无权限")
        
        total_amount = Decimal("0.00")
        order_items = []
        
        for item in items:
            product = self.db.query(Product).filter(
                Product.id == item["product_id"],
                Product.is_active == True
            ).first()
            if not product:
                raise Exception(f"商品 {item['product_id']} 不存在或已下架")
            
            if product.stock < item["quantity"]:
                raise Exception(f"商品 {product.name} 库存不足")
            
            item_price = Decimal(str(item["price"]))
            item_total = item_price * item["quantity"]
            total_amount += item_total
            
            order_item = OrderItem(
                product_id=product.id,
                quantity=item["quantity"],
                price=item_price
            )
            order_items.append(order_item)
        
        order = Order(
            order_no=self.generate_order_no(),
            user_id=user_id,
            address_id=address_id,
            total_amount=total_amount,
            status="pending",
            remark=remark
        )
        order.items = order_items
        
        for item in items:
            product = self.db.query(Product).filter(Product.id == item["product_id"]).first()
            product.stock -= item["quantity"]
        
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        
        return order
    
    def get_user_orders(self, user_id: int, skip: int = 0, limit: int = 100) -> list:
        """获取用户订单列表"""
        orders = self.db.query(Order).filter(
            Order.user_id == user_id
        ).order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
        return orders
    
    def get_order_by_id(self, order_id: int, user_id: int = None) -> Order:
        """获取订单详情"""
        query = self.db.query(Order).filter(Order.id == order_id)
        if user_id:
            query = query.filter(Order.user_id == user_id)
        order = query.first()
        if not order:
            raise Exception("订单不存在")
        return order
    
    def cancel_order(self, order_id: int, user_id: int) -> Order:
        """取消订单"""
        order = self.get_order_by_id(order_id, user_id)
        
        if order.status not in ["pending", "paid"]:
            raise Exception("订单状态不允许取消")
        
        for item in order.items:
            product = self.db.query(Product).filter(Product.id == item.product_id).first()
            if product:
                product.stock += item.quantity
        
        order.status = "cancelled"
        self.db.commit()
        self.db.refresh(order)
        
        return order
    
    def update_order_status(self, order_id: int, status: str, user_id: int = None) -> Order:
        """更新订单状态"""
        order = self.get_order_by_id(order_id, user_id)
        order.status = status
        
        if status == "paid":
            order.payment_time = datetime.now()
        elif status == "delivered":
            order.delivery_time = datetime.now()
        
        self.db.commit()
        self.db.refresh(order)
        
        return order

