"""订单相关 API"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.order import OrderCreate
from app.utils.dependencies import get_current_user, get_verified_user
from app.models.user import User
from app.models.product import Product
from app.models.address import Address
from app.services.order_service import OrderService
from app.utils.response import success_response, error_response, handle_errors

router = APIRouter()


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
    
    # 加载订单项的商品信息
    if db:
        for item in order.items:
            product = db.query(Product).filter(Product.id == item.product_id).first()
            item_dict = {
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": float(item.price) if item.price else 0.0
            }
            if product:
                item_dict["product_name"] = product.name
                item_dict["product_image"] = product.image_url
            order_dict["items"].append(item_dict)
    else:
        for item in order.items:
            order_dict["items"].append({
                "id": item.id,
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": float(item.price) if item.price else 0.0
            })
    
    return order_dict


@router.post("/")
@handle_errors
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_verified_user),
    db: Session = Depends(get_db)
):
    """创建订单（需要已验证手机号）"""
    order_service = OrderService(db)
    items = [item.model_dump() for item in order_data.items]
    order = order_service.create_order(
        user_id=current_user.id,
        address_id=order_data.address_id,
        items=items,
        remark=order_data.remark
    )
    db.refresh(order)
    return success_response(data=order_to_dict(order, db), message="订单创建成功")


@router.get("/")
@handle_errors
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户订单列表"""
    order_service = OrderService(db)
    orders = order_service.get_user_orders(current_user.id, skip, limit)
    return success_response(data=[order_to_dict(order, db) for order in orders], message="获取成功")


@router.get("/{order_id}")
@handle_errors
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取订单详情"""
    order_service = OrderService(db)
    order = order_service.get_order_by_id(order_id, current_user.id)
    
    order_dict = order_to_dict(order, db)
    
    # 加载收货地址信息
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


@router.put("/{order_id}/cancel")
@handle_errors
async def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消订单"""
    order_service = OrderService(db)
    order = order_service.cancel_order(order_id, current_user.id)
    return success_response(data=order_to_dict(order), message="订单已取消")
