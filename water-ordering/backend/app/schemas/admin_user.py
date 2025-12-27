"""后台管理员用户相关的 Pydantic 模式"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AdminLogin(BaseModel):
    """后台管理员登录请求"""
    username: str
    password: str


class AdminUserResponse(BaseModel):
    """后台管理员用户响应"""
    id: int
    username: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    old_password: str
    new_password: str

