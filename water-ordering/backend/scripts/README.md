# Scripts 目录说明

## 文件列表

### init_admin_user.py
**用途**：创建初始管理员用户  
**说明**：由于密码需要使用 bcrypt 加密，此脚本用于创建管理员用户  
**使用方法**：
```bash
# 创建默认管理员（用户名: admin, 密码: admin123）
python scripts/init_admin_user.py

# 指定用户名和密码
python scripts/init_admin_user.py --username admin --password your_password
```

### init_data.py
**用途**：初始化测试商品数据  
**说明**：用于开发和测试，创建示例商品数据  
**使用方法**：
```bash
# 添加测试商品
python scripts/init_data.py

# 清空所有商品数据（谨慎使用）
python scripts/init_data.py --clear
```

## 注意事项

1. **数据库表创建**：请使用 `database/init.sql` 文件手动创建表，不要使用 Python 脚本
2. **管理员创建**：由于密码加密需要，建议使用 `init_admin_user.py` 脚本创建
3. **测试数据**：测试数据也可以通过 `database/test_data.sql` 文件手动插入

## 数据库操作原则

**所有业务数据的增删改查都通过 API 接口进行：**
- 用户数据：通过 `/api/auth/*` 和 `/api/users/*` 接口
- 管理员数据：通过 `/api/admin-auth/*` 接口
- 商品数据：通过 `/api/products/*` 接口
- 订单数据：通过 `/api/orders/*` 接口
- 地址数据：通过 `/api/addresses/*` 接口

**不要直接操作数据库进行业务数据的增删改查。**

