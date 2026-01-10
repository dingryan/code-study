"""
初始化测试数据脚本
创建示例商品数据
"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.product import Product
from decimal import Decimal
from sqlalchemy import text  # 在顶部导入


def init_test_data():
    """初始化测试数据"""
    db = SessionLocal()
    
    try:
        # 先测试连接
        print("正在连接数据库...")
        db.execute(text("SELECT 1"))
        print("✅ 数据库连接成功")
        
        # 检查表是否存在
        print("正在检查数据表...")
        result = db.execute(text("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = DATABASE() AND table_name = 'products'
        """))
        table_exists = result.scalar() > 0
        if not table_exists:
            print("❌ products 表不存在，请先执行数据库初始化：")
            print("   mysql -u用户名 -p < database/init.sql")
            print("   或在 MySQL 客户端中：source database/init.sql")
            return
        
        # 检查是否已有数据
        existing_products = db.query(Product).count()
        print(f"当前数据库中有 {existing_products} 个商品")
        if existing_products > 0:
            print(f"是否继续添加？(y/n): ", end="")
            choice = input().strip().lower()
            if choice != 'y':
                print("已取消操作")
                return
        
        # 创建测试商品数据
        products = [
            {
                "name": "18.9L 桶装水",
                "description": "优质纯净水，适合家庭和办公室使用",
                "price": Decimal("15.00"),
                "image_url": "",  # 使用空字符串，小程序会显示默认占位图
                "stock": 100,
                "is_active": True
            },
            {
                "name": "12L 桶装水",
                "description": "小容量桶装水，适合小家庭使用",
                "price": Decimal("12.00"),
                "image_url": "https://via.placeholder.com/300x300?text=12L+桶装水",
                "stock": 80,
                "is_active": True
            },
            {
                "name": "5L 桶装水",
                "description": "便携式小桶装水，方便携带",
                "price": Decimal("8.00"),
                "image_url": "https://via.placeholder.com/300x300?text=5L+桶装水",
                "stock": 150,
                "is_active": True
            },
            {
                "name": "矿泉水 24瓶装",
                "description": "500ml 瓶装矿泉水，24瓶一箱",
                "price": Decimal("35.00"),
                "image_url": "https://via.placeholder.com/300x300?text=矿泉水+24瓶装",
                "stock": 200,
                "is_active": True
            },
            {
                "name": "纯净水 12瓶装",
                "description": "550ml 瓶装纯净水，12瓶一箱",
                "price": Decimal("20.00"),
                "image_url": "https://via.placeholder.com/300x300?text=纯净水+12瓶装",
                "stock": 180,
                "is_active": True
            },
            {
                "name": "高端矿泉水 6瓶装",
                "description": "1L 高端矿泉水，6瓶装，适合商务场合",
                "price": Decimal("88.00"),
                "image_url": "https://via.placeholder.com/300x300?text=高端矿泉水",
                "stock": 50,
                "is_active": True
            },
            {
                "name": "苏打水 12瓶装",
                "description": "500ml 苏打水，12瓶装，清爽口感",
                "price": Decimal("28.00"),
                "image_url": "https://via.placeholder.com/300x300?text=苏打水+12瓶装",
                "stock": 120,
                "is_active": True
            },
            {
                "name": "运动饮料 24瓶装",
                "description": "500ml 运动饮料，24瓶装，补充电解质",
                "price": Decimal("45.00"),
                "image_url": "https://via.placeholder.com/300x300?text=运动饮料",
                "stock": 100,
                "is_active": True
            }
        ]
        
        # 添加商品到数据库
        added_count = 0
        for product_data in products:
            # 检查商品是否已存在（根据名称）
            existing = db.query(Product).filter(Product.name == product_data["name"]).first()
            if existing:
                print(f"商品 '{product_data['name']}' 已存在，跳过")
                continue
            
            product = Product(**product_data)
            db.add(product)
            added_count += 1
        
        db.commit()
        print(f"\n✅ 成功添加 {added_count} 个测试商品！")
        print("\n商品列表：")
        all_products = db.query(Product).filter(Product.is_active == True).all()
        for p in all_products:
            print(f"  - {p.name}: ¥{p.price} (库存: {p.stock})")
        
    except Exception as e:
        db.rollback()
        print(f"❌ 错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def clear_test_data():
    """清空测试数据（谨慎使用）"""
    db = SessionLocal()
    try:
        print("警告：即将删除所有商品数据！")
        confirm = input("确认删除？(yes/no): ")
        if confirm.lower() == "yes":
            count = db.query(Product).count()
            db.query(Product).delete()
            db.commit()
            print(f"✅ 已删除 {count} 个商品")
        else:
            print("操作已取消")
    except Exception as e:
        db.rollback()
        print(f"❌ 错误: {str(e)}")
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="初始化测试数据工具")
    parser.add_argument("--clear", action="store_true", help="清空所有测试数据")
    args = parser.parse_args()
    
    if args.clear:
        clear_test_data()
    else:
        init_test_data()

