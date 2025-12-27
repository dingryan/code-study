# 网上订水系统

一个完整的网上订水系统，包含小程序端（用户下单）和Web后台（管理员管理）。

## 项目结构

```
water-ordering/
├── backend/          # Python FastAPI 后端
├── miniprogram/      # 微信小程序（用户端）
├── web-admin/        # React Web后台（管理端）
└── docs/             # 项目文档
    ├── 01-需求文档.md
    ├── 02-使用手册.md
    └── 03-API接口文档.md
```

## 技术栈

- **后端**：FastAPI + MySQL + SQLAlchemy + JWT
- **小程序**：微信小程序原生开发
- **Web后台**：React + Vite + React Router

## 快速开始

### 1. 启动后端

```bash
cd water-ordering/backend
pip install -r requirements.txt

# 初始化数据库（在 MySQL 中执行）
mysql -u用户名 -p < database/init.sql

# 创建初始管理员（可选）
python scripts/init_admin_user.py

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 启动Web后台

```bash
cd water-ordering/web-admin
npm install
npm run dev
```

### 3. 启动小程序

在微信开发者工具中导入 `water-ordering/miniprogram` 目录

## 功能特性

### 小程序端（用户）
- ✅ 手机号验证码登录
- ✅ 商品浏览（无需登录）
- ✅ 购物车管理
- ✅ 订单创建和查询
- ✅ 地址管理
- ✅ 权限控制（未登录只能浏览，不能下单）

### Web后台（管理员）
- ✅ 商品管理（增删改查、上下架、库存）
- ✅ 订单管理（查看订单列表和详情）

## 文档

详细文档请查看 `docs/` 目录：

- **[需求文档](docs/01-需求文档.md)** - 功能需求和技术要求
- **[使用手册](docs/02-使用手册.md)** - 快速上手指南
- **[API接口文档](docs/03-API接口文档.md)** - 接口说明和业务逻辑
- **[业务逻辑说明](docs/04-业务逻辑说明.md)** - 核心业务逻辑详解
- **[数据库文档](docs/05-数据库文档.md)** - 数据库表结构和维护

查看 [文档目录](docs/README.md) 了解所有文档

## 访问地址

- **后端API**：http://localhost:8000
- **API文档**：http://localhost:8000/docs
- **Web后台**：http://localhost:5173

## 配置说明

### 数据库配置

编辑 `backend/config/config.yaml`：
```yaml
database_url: "mysql+pymysql://用户名:密码@localhost:3306/water_ordering?charset=utf8mb4"
environment: "dev"  # dev开发环境, prod生产环境
code_expire_minutes: 5  # 验证码有效期（分钟）
```

### 小程序配置

编辑 `miniprogram/app.js`：
```javascript
apiBaseUrl: 'http://localhost:8000'  // 开发环境
```

### Web后台配置

编辑 `web-admin/.env.development`：
```env
VITE_API_BASE_URL=http://localhost:8000
```

## 常见问题

### 数据库字段缺失

如果遇到 `phone_verified` 或 `openid` 字段错误，执行：

```sql
ALTER TABLE users ADD COLUMN phone_verified BOOLEAN DEFAULT FALSE COMMENT '手机号是否已验证';
ALTER TABLE users MODIFY COLUMN openid VARCHAR(100) NULL COMMENT '微信 openid（可选）';
```

### 验证码获取

开发环境下，验证码会在后端控制台打印，前端会自动回填。

### 创建管理员用户

```bash
cd water-ordering/backend
python scripts/init_admin_user.py --username admin --password your_password
```

默认管理员账号：`admin` / `admin123`（请登录后立即修改密码）

**注意**：数据库表需要通过 `database/init.sql` 手动创建

## 更多信息

- 查看 [快速参考](快速参考.md) 获取常用命令
- 查看 [docs/](docs/) 目录获取详细文档
