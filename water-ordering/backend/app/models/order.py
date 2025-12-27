"""订单数据模型"""

from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Order(Base):
    """订单表"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_no = Column(String(50), unique=True, index=True, nullable=False, comment="订单号")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户 ID")
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=False, comment="地址 ID")
    total_amount = Column(Numeric(10, 2), nullable=False, comment="订单总金额")
    status = Column(String(20), default="pending", comment="订单状态: pending, paid, shipped, delivered, cancelled")
    payment_method = Column(String(20), comment="支付方式")
    payment_time = Column(DateTime, comment="支付时间")
    delivery_time = Column(DateTime, comment="配送时间")
    remark = Column(String(500), comment="备注")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    user = relationship("User", backref="orders")
    address = relationship("Address", backref="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    """订单项表"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, comment="订单 ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="商品 ID")
    quantity = Column(Integer, nullable=False, comment="数量")
    price = Column(Numeric(10, 2), nullable=False, comment="单价")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

