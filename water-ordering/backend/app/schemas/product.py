"""商品相关的 Pydantic 模式"""

from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from typing import Optional


class ProductResponse(BaseModel):
    """商品响应"""
    id: int
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None
    stock: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    """创建商品"""
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None
    stock: int = 0
    is_active: bool = True


class ProductUpdate(BaseModel):
    """更新商品"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    image_url: Optional[str] = None
    stock: Optional[int] = None
    is_active: Optional[bool] = None


class ProductStockUpdate(BaseModel):
    """更新库存"""
    stock: int


class ProductToggle(BaseModel):
    """上架/下架"""
    is_active: bool

