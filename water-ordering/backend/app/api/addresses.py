"""地址相关 API"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.address import AddressCreate, AddressUpdate
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.models.address import Address
from app.utils.response import success_response, error_response, handle_errors

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
@handle_errors
async def get_addresses(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取用户地址列表"""
    addresses = db.query(Address).filter(Address.user_id == current_user.id).all()
    return success_response(data=[address_to_dict(addr) for addr in addresses], message="获取成功")


@router.post("/")
@handle_errors
async def create_address(
    address_data: AddressCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建地址"""
    # 如果设置为默认地址，取消其他默认地址
    if address_data.is_default:
        db.query(Address).filter(
            Address.user_id == current_user.id,
            Address.is_default == True
        ).update({"is_default": False})
    
    address = Address(user_id=current_user.id, **address_data.model_dump())
    db.add(address)
    db.commit()
    db.refresh(address)
    
    return success_response(data=address_to_dict(address), message="创建成功")


@router.get("/{address_id}")
@handle_errors
async def get_address(
    address_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取地址详情"""
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == current_user.id
    ).first()
    if not address:
        return error_response(code=404, message="地址不存在")
    return success_response(data=address_to_dict(address), message="获取成功")


@router.put("/{address_id}")
@handle_errors
async def update_address(
    address_id: int,
    address_data: AddressUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新地址"""
    address = db.query(Address).filter(
        Address.id == address_id,
        Address.user_id == current_user.id
    ).first()
    if not address:
        return error_response(code=404, message="地址不存在")
    
    update_data = address_data.model_dump(exclude_unset=True)
    # 如果设置为默认地址，取消其他默认地址
    if update_data.get("is_default"):
        db.query(Address).filter(
            Address.user_id == current_user.id,
            Address.is_default == True,
            Address.id != address_id
        ).update({"is_default": False})
    
    for key, value in update_data.items():
        setattr(address, key, value)
    
    db.commit()
    db.refresh(address)
    
    return success_response(data=address_to_dict(address), message="更新成功")


@router.delete("/{address_id}")
@handle_errors
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
