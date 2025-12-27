"""地址相关 API"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.address import AddressCreate, AddressUpdate
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.models.address import Address
from app.utils.response import success_response, error_response

router = APIRouter()


def address_to_dict(address: Address) -> dict:
    """将地址对象转换为字典"""
    return {
        "id": address.id,
        "user_id": address.user_id,
        "name": address.name,
        "phone": address.phone,
        "province": address.province,
        "city": address.city,
        "district": address.district,
        "detail": address.detail,
        "is_default": address.is_default,
        "created_at": address.created_at.isoformat() if address.created_at else None,
        "updated_at": address.updated_at.isoformat() if address.updated_at else None
    }


@router.get("/")
async def get_addresses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户地址列表"""
    try:
        addresses = db.query(Address).filter(Address.user_id == current_user.id).all()
        address_list = [address_to_dict(addr) for addr in addresses]
        return success_response(data=address_list, message="获取成功")
    except Exception as e:
        return error_response(code=500, message=f"获取地址列表失败: {str(e)}")


@router.post("/")
async def create_address(
    address_data: AddressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建地址"""
    try:
        if address_data.is_default:
            db.query(Address).filter(
                Address.user_id == current_user.id,
                Address.is_default == True
            ).update({"is_default": False})
        
        address = Address(
            user_id=current_user.id,
            **address_data.model_dump()
        )
        db.add(address)
        db.commit()
        db.refresh(address)
        
        address_dict = address_to_dict(address)
        return success_response(data=address_dict, message="创建成功")
    except Exception as e:
        db.rollback()
        return error_response(code=500, message=f"创建地址失败: {str(e)}")


@router.get("/{address_id}")
async def get_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取地址详情"""
    try:
        address = db.query(Address).filter(
            Address.id == address_id,
            Address.user_id == current_user.id
        ).first()
        if not address:
            return error_response(code=404, message="地址不存在")
        address_dict = address_to_dict(address)
        return success_response(data=address_dict, message="获取成功")
    except Exception as e:
        return error_response(code=500, message=f"获取地址详情失败: {str(e)}")


@router.put("/{address_id}")
async def update_address(
    address_id: int,
    address_data: AddressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新地址"""
    try:
        address = db.query(Address).filter(
            Address.id == address_id,
            Address.user_id == current_user.id
        ).first()
        if not address:
            return error_response(code=404, message="地址不存在")
        
        update_data = address_data.model_dump(exclude_unset=True)
        if "is_default" in update_data and update_data["is_default"]:
            db.query(Address).filter(
                Address.user_id == current_user.id,
                Address.is_default == True,
                Address.id != address_id
            ).update({"is_default": False})
        
        for key, value in update_data.items():
            setattr(address, key, value)
        
        db.commit()
        db.refresh(address)
        
        address_dict = address_to_dict(address)
        return success_response(data=address_dict, message="更新成功")
    except Exception as e:
        db.rollback()
        return error_response(code=500, message=f"更新地址失败: {str(e)}")


@router.delete("/{address_id}")
async def delete_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除地址"""
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == current_user.id
    ).first()
    if not address:
        return error_response(code=404, message="地址不存在")
    
    db.delete(address)
    db.commit()
    
    return success_response(message="删除成功")

