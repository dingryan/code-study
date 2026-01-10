"""认证相关 API"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import SendCodeRequest, PhoneLogin
from app.services.auth_service import AuthService
from app.utils.response import success_response, handle_errors

router = APIRouter()


@router.post("/send-code")
@handle_errors
async def send_code(request: SendCodeRequest, db: Session = Depends(get_db)):
    """发送验证码"""
    auth_service = AuthService(db)
    result = auth_service.send_verification_code(request.phone)
    return success_response(data=result, message="操作成功.")


@router.post("/phone-login")
@handle_errors
async def phone_login(login_data: PhoneLogin, db: Session = Depends(get_db)):
    """手机号验证码登录"""
    auth_service = AuthService(db)
    result = auth_service.phone_login(login_data.phone, login_data.code)
    return success_response(data=result, message="操作成功.")
