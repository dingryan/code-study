# API接口文档

## 基础信息

- **基础URL**：`http://localhost:8000`
- **API文档**：http://localhost:8000/docs
- **响应格式**：统一JSON格式

## 统一响应格式

### 成功响应
```json
{
  "code": "0",
  "data": {},
  "msg": "操作成功.",
  "requestId": "8df5b689613421bc"
}
```

### 失败响应
```json
{
  "code": "0",
  "data": {
    "error": "错误信息"
  },
  "msg": "错误原因",
  "requestId": "8df5b689613421bc"
}
```

## 认证接口

### 1. 发送验证码

**接口**：`POST /api/auth/send-code`

**权限**：公开

**请求参数**：
```json
{
  "phone": "18017807956"
}
```

**业务逻辑**：
1. 验证手机号格式（11位数字，以1开头）
2. 检查该手机号是否已有未过期的验证码
   - 如果有且未过期：返回相同验证码
   - 如果没有或已过期：生成新验证码（6位随机数字）
3. 存储验证码到内存（有效期5分钟）
4. 开发环境：返回验证码；生产环境：调用短信服务商（待实现）

**响应示例**：
```json
{
  "code": "0",
  "data": {
    "verifyCode": "123456"
  },
  "msg": "操作成功.",
  "requestId": "8df5b689613421bc"
}
```

### 2. 手机号验证码登录

**接口**：`POST /api/auth/phone-login`

**权限**：公开

**请求参数**：
```json
{
  "phone": "18017807956",
  "code": "123456"
}
```

**业务逻辑**：
1. 验证手机号格式
2. 验证验证码：
   - 检查该手机号是否有验证码记录
   - 检查验证码是否过期（5分钟）
   - 检查验证码是否正确
   - 验证成功后删除验证码（一次性使用）
3. 查找或创建用户：
   - 如果用户不存在：创建新用户，设置 `phone_verified=true`
   - 如果用户存在：更新 `phone_verified=true`
4. 生成JWT token
5. 返回token和用户信息

**响应示例**：
```json
{
  "code": "0",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "phone": "18017807956",
      "nickname": null,
      "phone_verified": true
    }
  },
  "msg": "操作成功.",
  "requestId": "8df5b689613421bc"
}
```

## 后台认证接口

### 1. 后台管理员登录

**接口**：`POST /api/admin-auth/login`

**权限**：公开

**请求参数**：
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**业务逻辑**：
1. 验证用户名和密码
2. 查询 `admin_users` 表中是否存在该用户名
3. 验证密码（使用 bcrypt 验证）
4. 如果用户名或密码错误，返回错误信息
5. 生成JWT token（包含用户ID、用户名、type="admin"）
6. 返回token和用户信息

**响应示例**：
```json
{
  "code": "0",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "username": "admin",
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00"
    }
  },
  "msg": "操作成功.",
  "requestId": "8df5b689613421bc"
}
```

**错误响应**：
```json
{
  "code": "0",
  "data": {
    "error": "用户名或密码错误"
  },
  "msg": "用户名或密码错误",
  "requestId": "8df5b689613421bc"
}
```

### 2. 修改密码

**接口**：`POST /api/admin-auth/change-password`

**权限**：需要后台管理员登录

**请求头**：
```
Authorization: Bearer {token}
```

**请求参数**：
```json
{
  "old_password": "admin123",
  "new_password": "newpassword123"
}
```

**业务逻辑**：
1. 验证token，获取当前管理员用户
2. 验证原密码是否正确
3. 验证新密码长度（至少6位）
4. 更新密码哈希
5. 返回成功信息

**响应示例**：
```json
{
  "code": "0",
  "data": null,
  "msg": "密码修改成功",
  "requestId": "8df5b689613421bc"
}
```

### 3. 获取当前管理员信息

**接口**：`GET /api/admin-auth/me`

**权限**：需要后台管理员登录

**请求头**：
```
Authorization: Bearer {token}
```

**业务逻辑**：
1. 验证token，获取当前管理员用户
2. 返回管理员信息（不包含密码）

**响应示例**：
```json
{
  "code": "0",
  "data": {
    "id": 1,
    "username": "admin",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  },
  "msg": "操作成功.",
  "requestId": "8df5b689613421bc"
}
```

## 用户接口

### 1. 获取当前用户信息

**接口**：`GET /api/users/me`

**权限**：需要登录

**请求头**：
```
Authorization: Bearer {token}
```

**业务逻辑**：
1. 从token中解析用户ID
2. 查询用户信息
3. 返回用户数据（不包含敏感信息）

**响应示例**：
```json
{
  "code": "0",
  "data": {
    "id": 1,
    "phone": "18017807956",
    "nickname": null,
    "phone_verified": true,
    "is_admin": false
  },
  "msg": "操作成功.",
  "requestId": "8df5b689613421bc"
}
```

### 2. 更新用户信息

**接口**：`PUT /api/users/me`

**权限**：需要登录

**请求参数**：
```json
{
  "nickname": "新昵称",
  "avatar_url": "https://example.com/avatar.jpg",
  "phone": "18017807957"
}
```

**业务逻辑**：
1. 验证token，获取当前用户
2. 更新用户信息（只更新提供的字段）
3. 保存到数据库
4. 返回更新后的用户信息

## 商品接口

### 1. 获取商品列表（公开）

**接口**：`GET /api/products/?skip=0&limit=100`

**权限**：公开

**业务逻辑**：
1. 查询所有上架的商品（`is_active=true`）
2. 支持分页（skip, limit）
3. 返回商品列表

**响应示例**：
```json
{
  "code": "0",
  "data": [
    {
      "id": 1,
      "name": "矿泉水",
      "description": "500ml装",
      "price": 10.00,
      "stock": 100,
      "image_url": "",
      "is_active": true
    }
  ],
  "msg": "操作成功.",
  "requestId": "8df5b689613421bc"
}
```

### 2. 获取商品详情（公开）

**接口**：`GET /api/products/{product_id}`

**权限**：公开

**业务逻辑**：
1. 根据ID查询商品
2. 如果商品不存在，返回404
3. 返回商品详情

### 3. 获取所有商品（管理员）

**接口**：`GET /api/products/admin/all?skip=0&limit=100`

**权限**：需要管理员权限

**业务逻辑**：
1. 验证管理员权限
2. 查询所有商品（包括上架和下架的）
3. 返回商品列表

### 4. 创建商品（管理员）

**接口**：`POST /api/products/`

**权限**：需要管理员权限

**请求参数**：
```json
{
  "name": "矿泉水",
  "description": "500ml装",
  "price": 10.00,
  "stock": 100,
  "image_url": "https://example.com/image.jpg",
  "is_active": true
}
```

**业务逻辑**：
1. 验证管理员权限
2. 创建商品记录
3. 保存到数据库
4. 返回创建的商品信息

### 5. 更新商品（管理员）

**接口**：`PUT /api/products/{product_id}`

**权限**：需要管理员权限

**业务逻辑**：
1. 验证管理员权限
2. 查询商品是否存在
3. 更新商品信息（只更新提供的字段）
4. 保存到数据库

### 6. 删除商品（管理员）

**接口**：`DELETE /api/products/{product_id}`

**权限**：需要管理员权限

**业务逻辑**：
1. 验证管理员权限
2. 查询商品是否存在
3. 删除商品记录
4. 返回成功信息

### 7. 上下架商品（管理员）

**接口**：`PATCH /api/products/{product_id}/toggle`

**权限**：需要管理员权限

**请求参数**：
```json
{
  "is_active": false
}
```

**业务逻辑**：
1. 验证管理员权限
2. 查询商品是否存在
3. 更新 `is_active` 字段
4. 保存到数据库

### 8. 更新库存（管理员）

**接口**：`PATCH /api/products/{product_id}/stock`

**权限**：需要管理员权限

**请求参数**：
```json
{
  "stock": 200
}
```

**业务逻辑**：
1. 验证管理员权限
2. 查询商品是否存在
3. 更新库存数量
4. 保存到数据库

## 订单接口

### 1. 创建订单

**接口**：`POST /api/orders/`

**权限**：需要已验证手机号（`phone_verified=true`）

**请求头**：
```
Authorization: Bearer {token}
```

**请求参数**：
```json
{
  "address_id": 1,
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "price": 10.00
    }
  ],
  "remark": "请尽快送达"
}
```

**业务逻辑**：
1. 验证用户是否已验证手机号（`phone_verified=true`）
2. 验证收货地址是否存在且属于当前用户
3. 验证商品：
   - 商品是否存在
   - 商品是否上架
   - 库存是否充足
4. 计算订单总金额
5. 创建订单记录
6. 创建订单项记录
7. 扣减商品库存
8. 生成订单号（格式：WO + 时间戳 + 6位随机数）
9. 返回订单信息

**响应示例**：
```json
{
  "code": "0",
  "data": {
    "id": 1,
    "order_no": "WO20240101120000123456",
    "total_amount": 20.00,
    "status": "pending",
    "items": [
      {
        "id": 1,
        "product_id": 1,
        "product_name": "矿泉水",
        "quantity": 2,
        "price": 10.00
      }
    ]
  },
  "msg": "操作成功.",
  "requestId": "8df5b689613421bc"
}
```

### 2. 获取订单列表

**接口**：`GET /api/orders/?skip=0&limit=100`

**权限**：需要登录

**业务逻辑**：
1. 验证token，获取当前用户
2. 查询该用户的所有订单
3. 按创建时间倒序排列
4. 支持分页
5. 返回订单列表

### 3. 获取订单详情

**接口**：`GET /api/orders/{order_id}`

**权限**：需要登录（只能查看自己的订单）

**业务逻辑**：
1. 验证token，获取当前用户
2. 查询订单是否存在
3. 验证订单是否属于当前用户
4. 加载订单项的商品信息
5. 加载收货地址信息
6. 返回订单详情

### 4. 取消订单

**接口**：`PUT /api/orders/{order_id}/cancel`

**权限**：需要登录（只能取消自己的订单）

**业务逻辑**：
1. 验证token，获取当前用户
2. 查询订单是否存在且属于当前用户
3. 检查订单状态（只能取消"pending"或"paid"状态的订单）
4. 恢复商品库存
5. 更新订单状态为"cancelled"
6. 返回订单信息

## 地址接口

### 1. 获取地址列表

**接口**：`GET /api/addresses/`

**权限**：需要登录

**业务逻辑**：
1. 验证token，获取当前用户
2. 查询该用户的所有地址
3. 返回地址列表

### 2. 创建地址

**接口**：`POST /api/addresses/`

**权限**：需要登录

**请求参数**：
```json
{
  "name": "张三",
  "phone": "18017807956",
  "province": "广东省",
  "city": "深圳市",
  "district": "南山区",
  "detail": "科技园路123号",
  "is_default": true
}
```

**业务逻辑**：
1. 验证token，获取当前用户
2. 如果设置为默认地址，将其他地址的 `is_default` 设为 `false`
3. 创建地址记录
4. 保存到数据库
5. 返回地址信息

### 3. 获取地址详情

**接口**：`GET /api/addresses/{address_id}`

**权限**：需要登录（只能查看自己的地址）

**业务逻辑**：
1. 验证token，获取当前用户
2. 查询地址是否存在且属于当前用户
3. 返回地址详情

### 4. 更新地址

**接口**：`PUT /api/addresses/{address_id}`

**权限**：需要登录（只能更新自己的地址）

**业务逻辑**：
1. 验证token，获取当前用户
2. 查询地址是否存在且属于当前用户
3. 如果设置为默认地址，将其他地址的 `is_default` 设为 `false`
4. 更新地址信息
5. 保存到数据库

### 5. 删除地址

**接口**：`DELETE /api/addresses/{address_id}`

**权限**：需要登录（只能删除自己的地址）

**业务逻辑**：
1. 验证token，获取当前用户
2. 查询地址是否存在且属于当前用户
3. 删除地址记录
4. 返回成功信息

## 支付接口

### 1. 支付订单（模拟）

**接口**：`POST /api/payment/pay`

**权限**：需要登录

**请求参数**：
```json
{
  "order_id": 1,
  "payment_method": "wechat"
}
```

**业务逻辑**：
1. 验证token，获取当前用户
2. 查询订单是否存在且属于当前用户
3. 检查订单状态（只能支付"pending"状态的订单）
4. 模拟支付（更新订单状态为"paid"）
5. 返回支付结果

**注意**：当前为模拟支付，生产环境需要集成真实支付接口

## 权限说明

### 依赖函数

- `get_current_user`：获取当前小程序登录用户（需要token，从users表）
- `get_verified_user`：获取已验证手机号的用户（需要token且phone_verified=true）
- `get_current_admin_user`：获取当前后台管理员用户（需要token，从admin_users表）
- `get_admin_user`：获取管理员用户（别名，等同于get_current_admin_user）

### 权限矩阵

| 接口 | 权限要求 |
|------|---------|
| 发送验证码 | 公开 |
| 手机号登录 | 公开 |
| 商品列表 | 公开 |
| 商品详情 | 公开 |
| 用户信息 | 需要登录 |
| 地址管理 | 需要登录 |
| 订单查询 | 需要登录 |
| 创建订单 | 需要已验证手机号 |
| 商品管理 | 需要后台管理员（admin_users表） |
| 订单管理 | 需要后台管理员（admin_users表） |
| 后台认证 | 公开（登录）或需要后台管理员（其他操作） |

## 错误码说明

- `code: "0"`：操作成功
- `msg`：成功时"操作成功."，失败时返回具体错误原因

## 上传接口

### 1. 上传图片（管理员）

**接口**：`POST /api/upload/image`

**权限**：需要管理员权限

**请求格式**：`multipart/form-data`

**请求参数**：
- `file`: 图片文件（FormData）

**业务逻辑**：
1. 验证管理员权限
2. 验证文件类型（必须是图片）
3. 生成唯一文件名（UUID）
4. 保存文件到 `backend/uploads/` 目录
5. 返回文件访问URL

**响应示例**：
```json
{
  "code": "0",
  "data": {
    "url": "http://localhost:8000/static/xxx.jpg"
  },
  "msg": "操作成功.",
  "requestId": "8df5b689613421bc"
}
```

## 注意事项

1. 所有接口统一返回200状态码，通过 `code` 和 `msg` 判断成功失败
2. 需要认证的接口，请求头需携带：`Authorization: Bearer {token}`
3. 验证码有效期5分钟，一次性使用
4. 订单创建需要用户已验证手机号
5. 商品管理需要管理员权限
6. 验证码5分钟内同一手机号返回相同验证码

