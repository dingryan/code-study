"""初始化管理员用户"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.admin_user import AdminUser
from app.services.admin_auth_service import AdminAuthService

def init_admin_user(username: str = "admin", password: str = "admin123"):
    """初始化管理员用户"""
    db: Session = SessionLocal()
    try:
        # 检查用户是否已存在
        existing_user = db.query(AdminUser).filter(AdminUser.username == username).first()
        if existing_user:
            print(f"用户 {username} 已存在")
            return
        
        # 创建管理员用户
        auth_service = AdminAuthService(db)
        password_hash = auth_service.get_password_hash(password)
        
        admin_user = AdminUser(
            username=username,
            password_hash=password_hash
        )
        db.add(admin_user)
        db.commit()
        print(f"✅ 成功创建管理员用户: {username}")
        print(f"   默认密码: {password}")
        print(f"   请登录后立即修改密码！")
    except Exception as e:
        print(f"❌ 创建管理员用户失败: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="初始化管理员用户")
    parser.add_argument("--username", default="admin", help="用户名（默认: admin）")
    parser.add_argument("--password", default="admin123", help="密码（默认: admin123）")
    args = parser.parse_args()
    
    init_admin_user(args.username, args.password)

