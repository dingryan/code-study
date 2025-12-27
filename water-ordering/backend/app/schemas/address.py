"""地址相关的 Pydantic 模式"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AddressBase(BaseModel):
    """地址基础信息"""
    name: str
    phone: str
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    detail: str
    is_default: bool = False


class AddressCreate(AddressBase):
    """创建地址"""
    pass


class AddressUpdate(BaseModel):
    """更新地址"""
    name: Optional[str] = None
    phone: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    detail: Optional[str] = None
    is_default: Optional[bool] = None


class AddressResponse(AddressBase):
    """地址响应"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

