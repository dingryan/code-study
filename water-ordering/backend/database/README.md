# 数据库文件说明

## 文件列表

### init.sql
**用途**：数据库初始化脚本，包含所有表的创建语句  
**执行方式**：在 MySQL 客户端中手动执行  
**包含内容**：
- 创建数据库
- 创建所有表（users, admin_users, products, addresses, orders, order_items）
- 创建索引和外键约束
- 详细的注释说明

## 使用说明

### 1. 创建数据库和表

在 MySQL 客户端中执行：
```bash
mysql -u用户名 -p < backend/database/init.sql
```

或者在 MySQL 客户端中：
```sql
source backend/database/init.sql
```

### 2. 创建初始管理员

由于密码需要 bcrypt 加密，建议通过以下方式创建：

**方式1：使用接口创建（推荐）**
1. 启动后端服务
2. 使用接口 `POST /api/admin-auth/login` 测试登录
3. 如果不存在，可以通过接口创建（需要先实现创建接口）

**方式2：使用 Python 脚本**
```bash
cd backend
python scripts/init_admin_user.py --username admin --password admin123
```

**方式3：手动创建（需要先获取密码哈希）**
```python
# 运行以下代码获取密码哈希
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(pwd_context.hash("admin123"))
```

然后在 MySQL 中执行：
```sql
INSERT INTO admin_users (username, password_hash) 
VALUES ('admin', '上面获取的密码哈希');
```

## 注意事项

1. **字符集**：所有表使用 `utf8mb4` 字符集，支持 emoji 等特殊字符
2. **外键约束**：订单和地址表有外键约束，删除用户时会级联删除相关数据
3. **密码安全**：管理员密码使用 bcrypt 加密，不可逆
4. **表关系**：
   - `users` 和 `admin_users` 完全独立
   - `orders` 关联 `users` 和 `addresses`
   - `order_items` 关联 `orders` 和 `products`

## 数据库操作说明

**所有数据库的增删改查操作都通过 API 接口进行：**

- **用户数据**：通过 `/api/auth/*` 和 `/api/users/*` 接口
- **管理员数据**：通过 `/api/admin-auth/*` 接口
- **商品数据**：通过 `/api/products/*` 接口
- **订单数据**：通过 `/api/orders/*` 接口
- **地址数据**：通过 `/api/addresses/*` 接口

**不要直接操作数据库**，所有数据操作都应该通过接口进行。

