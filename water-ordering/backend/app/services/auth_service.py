"""认证服务"""

from sqlalchemy.orm import Session
from app.models.user import User
from app.services.sms_service import SMSService
from app.utils.jwt_handler import create_access_token


class AuthService:
    """认证服务类"""
    
    def __init__(self, db: Session):
        self.db = db
        self.sms_service = SMSService()
    
    def send_verification_code(self, phone: str) -> dict:
        """发送验证码"""
        # 验证手机号格式
        if not phone or len(phone) != 11 or not phone.isdigit():
            raise Exception("手机号格式不正确")
        
        # 发送验证码
        code = self.sms_service.send_code(phone)
        
        # 返回验证码（开发环境）
        return {
            "verifyCode": code
        }
    
    def phone_login(self, phone: str, code: str) -> dict:
        """手机号验证码登录"""
        # 验证手机号格式
        if not phone or len(phone) != 11 or not phone.isdigit():
            raise Exception("手机号格式不正确")
        
        # 验证验证码
        if not self.sms_service.verify_code(phone, code):
            raise Exception("验证码错误或已过期")
        
        # 查找或创建用户
        user = self.db.query(User).filter(User.phone == phone).first()
        if not user:
            # 创建新用户，openid 设为 None（允许为空）
            user = User(
                phone=phone, 
                phone_verified=True,
                openid=None  # 明确设置为 None，因为不再使用微信登录
            )
            self.db.add(user)
        else:
            user.phone_verified = True
        
        self.db.commit()
        self.db.refresh(user)
        
        # 生成token
        token = create_access_token(data={"sub": str(user.id), "phone": phone})
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "phone": user.phone,
                "nickname": user.nickname,
                "phone_verified": user.phone_verified
            }
        }
    
    def get_current_user(self, user_id: int) -> User:
        """通过 user_id 获取用户"""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise Exception("用户不存在")
        return user

