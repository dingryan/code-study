"""后台管理员认证相关 API"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.admin_user import AdminLogin, ChangePasswordRequest
from app.services.admin_auth_service import AdminAuthService
from app.utils.response import success_response, handle_errors
from app.utils.dependencies import get_current_admin_user
from app.models.admin_user import AdminUser

router = APIRouter()


@router.post("/login")
@handle_errors
async def admin_login(login_data: AdminLogin, db: Session = Depends(get_db)):
    """后台管理员登录（用户名密码）"""
    auth_service = AdminAuthService(db)
    result = auth_service.login(login_data.username, login_data.password)
    return success_response(data=result, message="操作成功.")


@router.post("/change-password")
@handle_errors
async def change_password(
    password_data: ChangePasswordRequest,
    current_admin: AdminUser = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """修改密码"""
    auth_service = AdminAuthService(db)
    auth_service.change_password(
        current_admin.id,
        password_data.old_password,
        password_data.new_password
    )
    return success_response(data=None, message="密码修改成功")


@router.get("/me")
@handle_errors
async def get_admin_info(current_admin: AdminUser = Depends(get_current_admin_user)):
    """获取当前管理员信息"""
    return success_response(
        data={
            "id": current_admin.id,
            "username": current_admin.username,
            "created_at": current_admin.created_at.isoformat() if current_admin.created_at else None,
            "updated_at": current_admin.updated_at.isoformat() if current_admin.updated_at else None
        },
        message="操作成功."
    )
