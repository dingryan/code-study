"""用户相关的 Pydantic 模式"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SendCodeRequest(BaseModel):
    """发送验证码请求"""
    phone: str


class PhoneLogin(BaseModel):
    """手机号验证码登录请求"""
    phone: str
    code: str


class UserResponse(BaseModel):
    """用户响应"""
    id: int
    openid: Optional[str] = None
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    phone_verified: bool = False
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """用户信息更新"""
    nickname: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None

