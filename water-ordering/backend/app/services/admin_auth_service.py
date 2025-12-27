"""后台管理员认证服务"""

from sqlalchemy.orm import Session
from app.models.admin_user import AdminUser
from app.utils.jwt_handler import create_access_token
from passlib.context import CryptContext

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AdminAuthService:
    """后台管理员认证服务类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """获取密码哈希"""
        return pwd_context.hash(password)
    
    def authenticate(self, username: str, password: str) -> AdminUser:
        """验证用户名和密码"""
        admin_user = self.db.query(AdminUser).filter(AdminUser.username == username).first()
        if not admin_user:
            raise Exception("用户名或密码错误")
        
        if not self.verify_password(password, admin_user.password_hash):
            raise Exception("用户名或密码错误")
        
        return admin_user
    
    def login(self, username: str, password: str) -> dict:
        """后台管理员登录"""
        admin_user = self.authenticate(username, password)
        
        # 生成token
        token = create_access_token(data={"sub": str(admin_user.id), "username": username, "type": "admin"})
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": admin_user.id,
                "username": admin_user.username,
                "created_at": admin_user.created_at.isoformat() if admin_user.created_at else None,
                "updated_at": admin_user.updated_at.isoformat() if admin_user.updated_at else None
            }
        }
    
    def change_password(self, admin_user_id: int, old_password: str, new_password: str) -> bool:
        """修改密码"""
        admin_user = self.db.query(AdminUser).filter(AdminUser.id == admin_user_id).first()
        if not admin_user:
            raise Exception("用户不存在")
        
        # 验证旧密码
        if not self.verify_password(old_password, admin_user.password_hash):
            raise Exception("原密码错误")
        
        # 更新密码
        admin_user.password_hash = self.get_password_hash(new_password)
        self.db.commit()
        self.db.refresh(admin_user)
        
        return True
    
    def get_admin_user(self, admin_user_id: int) -> AdminUser:
        """通过ID获取管理员用户"""
        admin_user = self.db.query(AdminUser).filter(AdminUser.id == admin_user_id).first()
        if not admin_user:
            raise Exception("管理员用户不存在")
        return admin_user

