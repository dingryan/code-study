"""用户数据模型"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    openid = Column(String(100), unique=True, index=True, nullable=True, comment="微信 openid（可选）")
    nickname = Column(String(50), comment="昵称")
    avatar_url = Column(String(500), comment="头像 URL")
    phone = Column(String(20), unique=True, index=True, nullable=True, comment="手机号")
    phone_verified = Column(Boolean, default=False, comment="手机号是否已验证")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    is_active = Column(Boolean, default=True, comment="是否激活")
    is_admin = Column(Boolean, default=False, comment="是否管理员（已废弃，后台管理员使用admin_users表）")

