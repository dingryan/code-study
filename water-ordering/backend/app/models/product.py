"""商品数据模型"""

from sqlalchemy import Column, Integer, String, Numeric, Text, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base


class Product(Base):
    """商品表"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="商品名称")
    description = Column(Text, comment="商品描述")
    price = Column(Numeric(10, 2), nullable=False, comment="价格")
    image_url = Column(String(500), comment="商品图片")
    stock = Column(Integer, default=0, comment="库存")
    is_active = Column(Boolean, default=True, comment="是否上架")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")

