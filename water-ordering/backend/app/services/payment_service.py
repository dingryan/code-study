"""模拟支付服务"""

from sqlalchemy.orm import Session
from app.services.order_service import OrderService
from datetime import datetime


class PaymentService:
    """支付服务类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.order_service = OrderService(db)
    
    def mock_payment(self, order_id: int, user_id: int, payment_method: str = "wechat") -> dict:
        """模拟支付"""
        order = self.order_service.get_order_by_id(order_id, user_id)
        
        if order.status != "pending":
            raise Exception("订单状态不允许支付")
        
        order.status = "paid"
        order.payment_method = payment_method
        order.payment_time = datetime.now()
        
        self.db.commit()
        self.db.refresh(order)
        
        return {
            "order_id": order.id,
            "order_no": order.order_no,
            "status": order.status,
            "payment_method": payment_method,
            "payment_time": order.payment_time.isoformat(),
            "message": "支付成功（模拟）"
        }

