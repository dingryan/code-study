"""用户相关 API"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.utils.response import success_response, error_response

router = APIRouter()


def user_to_dict(user: User) -> dict:
    """将用户对象转换为字典"""
    return {
        "id": user.id,
        "openid": user.openid,
        "nickname": user.nickname,
        "avatar_url": user.avatar_url,
        "phone": user.phone,
        "phone_verified": user.phone_verified if hasattr(user, 'phone_verified') else False,
        "is_admin": user.is_admin if hasattr(user, 'is_admin') else False,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }


@router.get("/me")
async def get_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    try:
        user_data = user_to_dict(current_user)
        return success_response(data=user_data, message="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        return error_response(code=500, message=f"获取用户信息失败: {str(e)}")


@router.put("/me")
async def update_user_info(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    try:
        if user_update.nickname is not None:
            current_user.nickname = user_update.nickname
        if user_update.avatar_url is not None:
            current_user.avatar_url = user_update.avatar_url
        if user_update.phone is not None:
            current_user.phone = user_update.phone
        
        db.commit()
        db.refresh(current_user)
        user_data = user_to_dict(current_user)
        return success_response(data=user_data, message="更新成功")
    except Exception as e:
        db.rollback()
        return error_response(code=500, message=f"更新用户信息失败: {str(e)}")

