# 网上订水 - 后端 API

## 技术栈
- FastAPI - 现代、快速的 Web 框架
- SQLAlchemy - ORM 数据库操作
- MySQL - 数据库
- JWT - 用户认证
- Pydantic - 数据验证

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

1. 复制 `config/config.example.yaml` 为 `config/config.yaml`
2. 修改 `config/config.yaml` 中的配置信息：
   - 数据库连接信息
   - JWT 密钥（生产环境请使用强密钥）
   - 微信小程序 AppID 和 AppSecret

## 数据库初始化

1. 创建 MySQL 数据库：
```sql
CREATE DATABASE water_ordering CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. 运行初始化脚本创建表：
```bash
python scripts/init_db.py
```

## 运行

```bash
# 开发模式（自动重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 或直接运行
python -m app.main
```

## API 文档

启动后访问：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 接口说明

### 认证
- `POST /api/auth/wechat-login` - 微信登录
- `GET /api/auth/me` - 获取当前用户信息

### 用户
- `GET /api/users/me` - 获取用户信息
- `PUT /api/users/me` - 更新用户信息

### 商品
- `GET /api/products/` - 获取商品列表
- `GET /api/products/{product_id}` - 获取商品详情

### 订单
- `POST /api/orders/` - 创建订单
- `GET /api/orders/` - 获取订单列表
- `GET /api/orders/{order_id}` - 获取订单详情
- `PUT /api/orders/{order_id}/cancel` - 取消订单

### 地址
- `GET /api/addresses/` - 获取地址列表
- `POST /api/addresses/` - 创建地址
- `GET /api/addresses/{address_id}` - 获取地址详情
- `PUT /api/addresses/{address_id}` - 更新地址
- `DELETE /api/addresses/{address_id}` - 删除地址

### 支付
- `POST /api/payment/pay` - 支付订单（模拟支付）

## 注意事项

- 所有配置信息放在 YAML 文件中，不硬编码
- 使用相对路径读取配置文件
- 遵循代码约定：小写+下划线命名
- 支付接口为模拟实现，开发阶段不调用真实微信支付

