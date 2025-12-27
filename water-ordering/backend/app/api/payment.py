"""支付相关 API"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.services.payment_service import PaymentService
from app.utils.response import success_response, error_response

router = APIRouter()


class PaymentRequest(BaseModel):
    """支付请求"""
    order_id: int
    payment_method: str = "wechat"


@router.post("/pay")
async def pay_order(
    payment_data: PaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """支付订单（模拟支付）"""
    try:
        payment_service = PaymentService(db)
        result = payment_service.mock_payment(
            payment_data.order_id, 
            current_user.id, 
            payment_data.payment_method
        )
        return success_response(data=result, message="支付成功")
    except Exception as e:
        return error_response(code=400, message=str(e))

