-- ============================================
-- 网上订水系统 - 数据库初始化脚本
-- ============================================
-- 说明：此文件包含所有数据库表的创建语句
-- 执行方式：在 MySQL 客户端中执行此文件
-- 执行顺序：按顺序执行，不要跳过任何步骤
-- ============================================

-- 1. 创建数据库（如果不存在）
-- 注意：请根据实际情况修改数据库名称
CREATE DATABASE IF NOT EXISTS water_ordering 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE water_ordering;

-- ============================================
-- 2. 创建小程序用户表 (users)
-- ============================================
-- 说明：存储小程序端用户信息，包括手机号、微信信息等
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    openid VARCHAR(100) NULL UNIQUE COMMENT '微信 openid（可选，已废弃）',
    nickname VARCHAR(50) NULL COMMENT '昵称',
    avatar_url VARCHAR(500) NULL COMMENT '头像 URL',
    phone VARCHAR(20) NULL UNIQUE COMMENT '手机号',
    phone_verified BOOLEAN DEFAULT FALSE COMMENT '手机号是否已验证',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否激活',
    is_admin BOOLEAN DEFAULT FALSE COMMENT '是否管理员（已废弃，后台管理员使用admin_users表）',
    INDEX idx_openid (openid),
    INDEX idx_phone (phone)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='小程序用户表';

-- ============================================
-- 3. 创建后台管理员用户表 (admin_users)
-- ============================================
-- 说明：存储后台管理系统管理员信息，与小程序用户完全分离
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '管理员ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名（用于登录）',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希（bcrypt加密）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='后台管理员用户表';

-- ============================================
-- 4. 创建商品表 (products)
-- ============================================
-- 说明：存储商品信息，包括名称、价格、库存等
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '商品ID',
    name VARCHAR(100) NOT NULL COMMENT '商品名称',
    description TEXT NULL COMMENT '商品描述',
    price DECIMAL(10, 2) NOT NULL COMMENT '价格',
    image_url VARCHAR(500) NULL COMMENT '商品图片URL',
    stock INT DEFAULT 0 COMMENT '库存数量',
    is_active BOOLEAN DEFAULT TRUE COMMENT '是否上架',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='商品表';

-- ============================================
-- 5. 创建收货地址表 (addresses)
-- ============================================
-- 说明：存储用户的收货地址信息
CREATE TABLE IF NOT EXISTS addresses (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '地址ID',
    user_id INT NOT NULL COMMENT '用户ID',
    name VARCHAR(50) NOT NULL COMMENT '收货人姓名',
    phone VARCHAR(20) NOT NULL COMMENT '收货人电话',
    province VARCHAR(50) NULL COMMENT '省份',
    city VARCHAR(50) NULL COMMENT '城市',
    district VARCHAR(50) NULL COMMENT '区县',
    detail VARCHAR(200) NOT NULL COMMENT '详细地址',
    is_default BOOLEAN DEFAULT FALSE COMMENT '是否默认地址',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='收货地址表';

-- ============================================
-- 6. 创建订单表 (orders)
-- ============================================
-- 说明：存储订单主信息
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单ID',
    order_no VARCHAR(50) NOT NULL UNIQUE COMMENT '订单号（格式：WO + 时间戳 + 6位随机数）',
    user_id INT NOT NULL COMMENT '用户ID',
    address_id INT NOT NULL COMMENT '收货地址ID',
    total_amount DECIMAL(10, 2) NOT NULL COMMENT '订单总金额',
    status VARCHAR(20) DEFAULT 'pending' COMMENT '订单状态：pending(待支付), paid(已支付), delivered(已送达), cancelled(已取消)',
    payment_method VARCHAR(20) NULL COMMENT '支付方式',
    payment_time DATETIME NULL COMMENT '支付时间',
    delivery_time DATETIME NULL COMMENT '配送时间',
    remark VARCHAR(500) NULL COMMENT '备注',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_order_no (order_no),
    INDEX idx_user_id (user_id),
    INDEX idx_address_id (address_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (address_id) REFERENCES addresses(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单表';

-- ============================================
-- 7. 创建订单项表 (order_items)
-- ============================================
-- 说明：存储订单中的商品明细信息
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单项ID',
    order_id INT NOT NULL COMMENT '订单ID',
    product_id INT NOT NULL COMMENT '商品ID',
    quantity INT NOT NULL COMMENT '购买数量',
    price DECIMAL(10, 2) NOT NULL COMMENT '单价（下单时的价格）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id),
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='订单项表';

-- ============================================
-- 8. 创建初始管理员用户（可选）
-- ============================================
-- 说明：创建默认管理员账号
-- 注意：密码需要使用 bcrypt 加密，建议使用接口创建或使用 Python 脚本
-- 如果需要手动创建，请先运行以下 Python 代码获取密码哈希：
-- 
-- from passlib.context import CryptContext
-- pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
-- print(pwd_context.hash("admin123"))
--
-- 然后将获取的哈希值替换下面的 'YOUR_PASSWORD_HASH'
-- 
-- INSERT INTO admin_users (username, password_hash) 
-- VALUES ('admin', 'YOUR_PASSWORD_HASH')
-- ON DUPLICATE KEY UPDATE username=username;

-- ============================================
-- 数据库初始化完成
-- ============================================
-- 执行完成后，可以验证表是否创建成功：
-- SHOW TABLES;
-- 
-- 查看表结构：
-- DESCRIBE users;
-- DESCRIBE admin_users;
-- DESCRIBE products;
-- DESCRIBE addresses;
-- DESCRIBE orders;
-- DESCRIBE order_items;

