"""FastAPI 依赖注入"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.admin_user import AdminUser
from app.utils.jwt_handler import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/phone-login")
admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin-auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """获取当前登录用户"""
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证信息"
            )
        user = db.query(User).filter(User.id == int(user_id)).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在"
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


def get_current_admin_user(
    token: str = Depends(admin_oauth2_scheme),
    db: Session = Depends(get_db)
) -> AdminUser:
    """获取当前后台管理员用户"""
    try:
        payload = verify_token(token)
        admin_id = payload.get("sub")
        token_type = payload.get("type")
        
        if admin_id is None or token_type != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证信息"
            )
        
        admin_user = db.query(AdminUser).filter(AdminUser.id == int(admin_id)).first()
        if admin_user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="管理员用户不存在"
            )
        return admin_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


def get_admin_user(
    current_admin: AdminUser = Depends(get_current_admin_user)
) -> AdminUser:
    """获取当前管理员用户（别名，保持兼容性）"""
    return current_admin


def get_verified_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """获取已验证手机号的用户"""
    if not current_user.phone_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="请先验证手机号"
        )
    return current_user

