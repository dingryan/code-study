"""商品相关 API"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product
from app.models.admin_user import AdminUser
from app.schemas.product import ProductCreate, ProductUpdate, ProductStockUpdate, ProductToggle
from app.utils.dependencies import get_admin_user
from app.utils.response import success_response, error_response, handle_errors

router = APIRouter()


def product_to_dict(product: Product) -> dict:
    """将商品对象转换为字典"""
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": float(product.price) if product.price else 0.0,
        "image_url": product.image_url,
        "stock": product.stock,
        "is_active": product.is_active,
        "created_at": product.created_at.isoformat() if product.created_at else None
    }


@router.get("/")
@handle_errors
async def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取上架商品列表"""
    products = db.query(Product).filter(Product.is_active == True).offset(skip).limit(limit).all()
    return success_response(data=[product_to_dict(p) for p in products], message="获取成功")


@router.get("/{product_id}")
@handle_errors
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """获取商品详情"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return error_response(code=404, message="商品不存在")
    return success_response(data=product_to_dict(product), message="获取成功")


@router.get("/admin/all")
@handle_errors
async def get_all_products(
    skip: int = 0,
    limit: int = 100,
    current_admin: AdminUser = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """获取所有商品（管理员）"""
    products = db.query(Product).offset(skip).limit(limit).all()
    return success_response(data=[product_to_dict(p) for p in products], message="获取成功")


@router.post("/")
@handle_errors
async def create_product(
    product_data: ProductCreate,
    current_admin: AdminUser = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """创建商品（管理员）"""
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return success_response(data=product_to_dict(product), message="创建成功")


@router.put("/{product_id}")
@handle_errors
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    current_admin: AdminUser = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """更新商品（管理员）"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return error_response(code=404, message="商品不存在")
    
    for key, value in product_data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return success_response(data=product_to_dict(product), message="更新成功")


@router.delete("/{product_id}")
@handle_errors
async def delete_product(
    product_id: int,
    current_admin: AdminUser = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """删除商品（管理员）"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return error_response(code=404, message="商品不存在")
    
    db.delete(product)
    db.commit()
    return success_response(data=None, message="删除成功")


@router.patch("/{product_id}/toggle")
@handle_errors
async def toggle_product(
    product_id: int,
    toggle_data: ProductToggle,
    current_admin: AdminUser = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """上下架商品（管理员）"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return error_response(code=404, message="商品不存在")
    
    product.is_active = toggle_data.is_active
    db.commit()
    db.refresh(product)
    return success_response(data=product_to_dict(product), message="操作成功")


@router.patch("/{product_id}/stock")
@handle_errors
async def update_stock(
    product_id: int,
    stock_data: ProductStockUpdate,
    current_admin: AdminUser = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    """更新商品库存（管理员）"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return error_response(code=404, message="商品不存在")
    
    product.stock = stock_data.stock
    db.commit()
    db.refresh(product)
    return success_response(data=product_to_dict(product), message="更新成功")
