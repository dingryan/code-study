"""订单相关 API"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.utils.dependencies import get_current_user, get_verified_user
from app.models.user import User
from app.models.product import Product
from app.models.address import Address
from app.services.order_service import OrderService
from app.utils.response import success_response, error_response

router = APIRouter()


def load_order_item_products(order_items, db: Session):
    """加载订单项的商品信息"""
    for item in order_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            item.product_name = product.name
            item.product_image = product.image_url


def order_to_dict(order, db: Session = None) -> dict:
    """将订单对象转换为字典"""
    order_dict = {
        "id": order.id,
        "order_no": order.order_no,
        "user_id": order.user_id,
        "address_id": order.address_id,
        "total_amount": float(order.total_amount) if order.total_amount else 0.0,
        "status": order.status,
        "payment_method": order.payment_method,
        "payment_time": order.payment_time.isoformat() if order.payment_time else None,
        "delivery_time": order.delivery_time.isoformat() if order.delivery_time else None,
        "remark": order.remark,
        "created_at": order.created_at.isoformat() if order.created_at else None,
        "updated_at": order.updated_at.isoformat() if order.updated_at else None,
        "items": []
    }
    
    if db:
        load_order_item_products(order.items, db)
    
    for item in order.items:
        item_dict = {
            "id": item.id,
            "product_id": item.product_id,
            "quantity": item.quantity,
            "price": float(item.price) if item.price else 0.0
        }
        if hasattr(item, 'product_name'):
            item_dict["product_name"] = item.product_name
        if hasattr(item, 'product_image'):
            item_dict["product_image"] = item.product_image
        order_dict["items"].append(item_dict)
    
    return order_dict


@router.post("/")
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_verified_user),
    db: Session = Depends(get_db)
):
    """创建订单（需要已验证手机号）"""
    try:
        order_service = OrderService(db)
        items = [item.model_dump() for item in order_data.items]
        order = order_service.create_order(
            user_id=current_user.id,
            address_id=order_data.address_id,
            items=items,
            remark=order_data.remark
        )
        db.refresh(order)
        order_dict = order_to_dict(order, db)
        return success_response(data=order_dict, message="订单创建成功")
    except Exception as e:
        db.rollback()
        import traceback
        traceback.print_exc()
        return error_response(code=400, message=str(e))


@router.get("/")
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户订单列表"""
    try:
        order_service = OrderService(db)
        orders = order_service.get_user_orders(current_user.id, skip, limit)
        order_list = [order_to_dict(order, db) for order in orders]
        return success_response(data=order_list, message="获取成功")
    except Exception as e:
        return error_response(code=500, message=f"获取订单列表失败: {str(e)}")


@router.get("/{order_id}")
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取订单详情"""
    try:
        order_service = OrderService(db)
        order = order_service.get_order_by_id(order_id, current_user.id)
        
        order_dict = order_to_dict(order, db)
        
        if order.address_id:
            address = db.query(Address).filter(Address.id == order.address_id).first()
            if address:
                order_dict["address"] = {
                    "id": address.id,
                    "name": address.name,
                    "phone": address.phone,
                    "province": address.province,
                    "city": address.city,
                    "district": address.district,
                    "detail": address.detail
                }
        
        return success_response(data=order_dict, message="获取成功")
    except Exception as e:
        return error_response(code=404, message=str(e))


@router.put("/{order_id}/cancel")
async def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消订单"""
    try:
        order_service = OrderService(db)
        order = order_service.cancel_order(order_id, current_user.id)
        order_dict = order_to_dict(order)
        return success_response(data=order_dict, message="订单已取消")
    except Exception as e:
        return error_response(code=400, message=str(e))

