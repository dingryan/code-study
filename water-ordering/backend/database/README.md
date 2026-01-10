# 数据库文档

## 快速开始

### 一键初始化（推荐）

**使用 complete_init.sql 完整初始化：**

在 Navicat 或 MySQL 客户端中执行：
```bash
mysql -u用户名 -p < complete_init.sql
```

**包含内容：**
- ✅ 数据库创建
- ✅ 所有表结构（7个表）
- ✅ 8个测试商品
- ✅ 默认管理员（用户名：admin，密码：admin123）
- ✅ 测试用户（手机号：13800138000）

### 分步初始化

```bash
# 1. 创建表结构
mysql -u用户名 -p < init.sql

# 2. 创建管理员（需要Python环境）
cd ../
python scripts/init_admin_user.py

# 3. 添加测试数据（可选）
python scripts/init_data.py
```

## 文件说明

| 文件 | 用途 | 说明 |
|------|------|------|
| `complete_init.sql` | 完整初始化 | 包含数据库、表、测试数据、管理员 |
| `init.sql` | 表结构初始化 | 只创建表结构，不含数据 |
| `test_data.sql` | 测试数据 | 测试商品数据 |
| `fix_phone_verified.sql` | 字段修复 | 修复缺失字段 |

## 数据库表

### 用户表 (users)
小程序用户表，存储用户基本信息
- 主键：id
- 唯一索引：phone
- 关键字段：phone_verified（手机验证状态）

### 管理员表 (admin_users)
后台管理员表，与用户表完全独立
- 主键：id
- 唯一索引：username
- 密码：bcrypt加密存储

### 商品表 (products)
商品信息表
- 主键：id
- 状态：is_active（上架/下架）
- 库存：stock

### 地址表 (addresses)
用户收货地址表
- 主键：id
- 外键：user_id（关联users表）
- 默认地址：is_default

### 订单表 (orders)
订单主表
- 主键：id
- 外键：user_id, address_id
- 状态：pending（待支付）、paid（已支付）、delivered（已送达）、cancelled（已取消）

### 订单明细表 (order_items)
订单商品明细
- 主键：id
- 外键：order_id, product_id

### 验证码表 (verification_codes)
手机验证码表
- 主键：id
- 唯一索引：phone
- 有效期：5分钟

## 数据库操作

### 重要原则

**所有业务数据的增删改查都通过 API 接口进行，不要直接操作数据库！**

- **用户数据**：通过 `/api/auth/*` 和 `/api/users/*` 接口
- **管理员数据**：通过 `/api/admin-auth/*` 接口
- **商品数据**：通过 `/api/products/*` 接口
- **订单数据**：通过 `/api/orders/*` 接口
- **地址数据**：通过 `/api/addresses/*` 接口

### 例外情况

以下情况可以直接操作数据库：
1. 数据库初始化
2. 数据迁移
3. 数据修复
4. 数据备份/恢复

## 常用操作

### 重置数据库
```sql
DROP DATABASE water_ordering;
```
然后重新执行 `complete_init.sql`

### 清空数据但保留表结构
```sql
TRUNCATE TABLE order_items;
TRUNCATE TABLE orders;
TRUNCATE TABLE addresses;
TRUNCATE TABLE products;
TRUNCATE TABLE users;
TRUNCATE TABLE admin_users;
```

### 修改管理员密码
登录后台在"修改密码"页面修改，或使用脚本：
```bash
cd ../
python scripts/init_admin_user.py --username admin --password new_password
```

## 注意事项

1. **字符集**: 使用 utf8mb4，支持 emoji
2. **外键约束**: 订单和地址有外键约束，删除用户会级联删除相关数据
3. **密码安全**: 管理员密码使用 bcrypt 加密，不可逆
4. **首次部署**: 执行 complete_init.sql 后立即修改管理员密码
