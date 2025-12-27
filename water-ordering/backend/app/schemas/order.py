"""订单相关的 Pydantic 模式"""

from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import List, Optional


class OrderItemCreate(BaseModel):
    """订单项创建"""
    product_id: int
    quantity: int
    price: Decimal


class OrderItemResponse(BaseModel):
    """订单项响应"""
    id: int
    product_id: int
    quantity: int
    price: Decimal
    product_name: Optional[str] = None
    product_image: Optional[str] = None
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """创建订单"""
    address_id: int
    items: List[OrderItemCreate]
    remark: Optional[str] = None


class OrderResponse(BaseModel):
    """订单响应"""
    id: int
    order_no: str
    user_id: int
    address_id: int
    total_amount: Decimal
    status: str
    payment_method: Optional[str] = None
    payment_time: Optional[datetime] = None
    delivery_time: Optional[datetime] = None
    remark: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemResponse] = []
    address: Optional[dict] = None
    
    class Config:
        from_attributes = True


class OrderUpdate(BaseModel):
    """更新订单"""
    status: Optional[str] = None
    payment_method: Optional[str] = None
    payment_time: Optional[datetime] = None
    delivery_time: Optional[datetime] = None

