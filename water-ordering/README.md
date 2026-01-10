# 网上订水系统

一个完整的网上订水系统，包含小程序端（用户下单）和Web后台（管理员管理）。

## 技术栈

- **后端**: FastAPI + MySQL + SQLAlchemy + JWT
- **小程序**: 微信小程序原生开发
- **Web后台**: React + Vite + React Router

## 快速开始

```bash
# 1. 初始化数据库（在MySQL客户端执行）
mysql -u用户名 -p < backend/database/complete_init.sql

# 2. 启动后端
cd backend
pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. 启动Web后台
cd web-admin
npm install
npm run dev

# 4. 启动小程序
# 在微信开发者工具中导入 miniprogram 目录
```

## 访问地址

- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **Web后台**: http://localhost:5173
- **默认管理员**: admin / admin123

## 项目结构

```
water-ordering/
├── backend/              # Python FastAPI 后端
│   ├── app/              # 应用代码
│   │   ├── api/          # API路由
│   │   ├── models/       # 数据模型
│   │   ├── services/     # 业务逻辑
│   │   └── utils/        # 工具函数
│   ├── config/           # 配置文件
│   ├── database/         # 数据库脚本
│   └── scripts/          # 初始化脚本
├── miniprogram/          # 微信小程序（用户端）
│   ├── pages/            # 页面
│   └── utils/            # 工具函数
├── web-admin/            # React Web后台（管理端）
│   └── src/
│       ├── pages/        # 页面组件
│       └── utils/        # 工具函数
└── docs/                 # 项目文档
    ├── 01-需求文档.md
    ├── 02-使用手册.md
    ├── 03-API接口文档.md
    ├── 04-业务逻辑说明.md
    └── 05-数据库文档.md
```

## 功能特性

### 小程序端（用户）
- ✅ 手机号验证码登录
- ✅ 商品浏览（无需登录）
- ✅ 购物车管理
- ✅ 订单创建和查询
- ✅ 地址管理
- ✅ 权限控制

### Web后台（管理员）
- ✅ 商品管理（增删改查、上下架、库存）
- ✅ 订单管理（查看订单列表和详情）
- ✅ 用户密码管理

## 详细文档

查看 [docs/](docs/) 目录获取完整文档：

- **[需求文档](docs/01-需求文档.md)** - 功能需求和技术架构
- **[使用手册](docs/02-使用手册.md)** - 环境搭建和使用指南
- **[API接口文档](docs/03-API接口文档.md)** - 接口说明和业务逻辑
- **[业务逻辑说明](docs/04-业务逻辑说明.md)** - 核心业务流程
- **[数据库文档](docs/05-数据库文档.md)** - 数据库设计和维护

## 配置说明

### 数据库配置
编辑 `backend/config/config.yaml`：
```yaml
database_url: "mysql+pymysql://用户名:密码@localhost:3306/water_ordering?charset=utf8mb4"
environment: "dev"
```

### 小程序配置
编辑 `miniprogram/app.js`：
```javascript
apiBaseUrl: 'http://localhost:8000'
```

### Web后台配置
编辑 `web-admin/.env.development`：
```env
VITE_API_BASE_URL=http://localhost:8000
```

## 常见问题

### 验证码获取
开发环境下，验证码会在后端控制台打印。

### 创建管理员
```bash
cd backend
python scripts/init_admin_user.py --username admin --password your_password
```

### 端口被占用
```bash
lsof -ti:8000 | xargs kill -9
```

更多问题请查看 [使用手册](docs/02-使用手册.md#故障排查)
