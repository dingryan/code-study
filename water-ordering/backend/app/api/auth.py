"""认证相关 API"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import SendCodeRequest, PhoneLogin
from app.services.auth_service import AuthService
from app.utils.response import success_response, error_response

router = APIRouter()


@router.post("/send-code")
async def send_code(
    request: SendCodeRequest,
    db: Session = Depends(get_db)
):
    """发送验证码"""
    try:
        auth_service = AuthService(db)
        result = auth_service.send_verification_code(request.phone)
        return success_response(data=result, message="操作成功.")
    except Exception as e:
        return error_response(message=str(e))


@router.post("/phone-login")
async def phone_login(
    login_data: PhoneLogin,
    db: Session = Depends(get_db)
):
    """手机号验证码登录"""
    try:
        auth_service = AuthService(db)
        result = auth_service.phone_login(login_data.phone, login_data.code)
        return success_response(data=result, message="操作成功.")
    except Exception as e:
        return error_response(message=str(e))

