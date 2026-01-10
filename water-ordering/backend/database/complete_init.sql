-- ============================================
-- 网上订水系统 - 完整数据库初始化脚本
-- ============================================
-- 说明：此文件包含所有表结构、测试数据和管理员账号
-- 适用场景：在新电脑上快速部署，可在 Navicat 中直接执行
-- 执行方式：在 MySQL 客户端或 Navicat 中执行此文件
-- 注意事项：执行前请确认数据库名称是否需要修改
-- ============================================

-- ============================================
-- 第一部分：创建数据库和表结构
-- ============================================

-- 1. 创建数据库（如果不存在）
CREATE DATABASE IF NOT EXISTS water_ordering 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE water_ordering;

-- 2. 创建小程序用户表 (users)
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

-- 3. 创建后台管理员用户表 (admin_users)
CREATE TABLE IF NOT EXISTS admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '管理员ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名（用于登录）',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希（bcrypt加密）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '修改时间',
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='后台管理员用户表';

-- 4. 创建商品表 (products)
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

-- 5. 创建收货地址表 (addresses)
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

-- 6. 创建订单表 (orders)
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

-- 7. 创建订单项表 (order_items)
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
-- 第二部分：插入测试商品数据
-- ============================================

-- 插入8个测试商品
-- 使用 INSERT IGNORE 避免重复插入
INSERT IGNORE INTO products (name, description, price, image_url, stock, is_active) VALUES
('18.9L 桶装水', '优质纯净水，适合家庭和办公室使用', 15.00, '', 100, TRUE),
('12L 桶装水', '小容量桶装水，适合小家庭使用', 12.00, 'https://via.placeholder.com/300x300?text=12L+桶装水', 80, TRUE),
('5L 桶装水', '便携式小桶装水，方便携带', 8.00, 'https://via.placeholder.com/300x300?text=5L+桶装水', 150, TRUE),
('矿泉水 24瓶装', '500ml 瓶装矿泉水，24瓶一箱', 35.00, 'https://via.placeholder.com/300x300?text=矿泉水+24瓶装', 200, TRUE),
('纯净水 12瓶装', '550ml 瓶装纯净水，12瓶一箱', 20.00, 'https://via.placeholder.com/300x300?text=纯净水+12瓶装', 180, TRUE),
('高端矿泉水 6瓶装', '1L 高端矿泉水，6瓶装，适合商务场合', 88.00, 'https://via.placeholder.com/300x300?text=高端矿泉水', 50, TRUE),
('苏打水 12瓶装', '500ml 苏打水，12瓶装，清爽口感', 28.00, 'https://via.placeholder.com/300x300?text=苏打水+12瓶装', 120, TRUE),
('运动饮料 24瓶装', '500ml 运动饮料，24瓶装，补充电解质', 45.00, 'https://via.placeholder.com/300x300?text=运动饮料', 100, TRUE);

-- ============================================
-- 第三部分：创建默认管理员账号
-- ============================================

-- 创建管理员账号
-- 用户名：admin
-- 密码：admin123
-- 注意：密码已使用 bcrypt 加密，下面的哈希值对应密码 "admin123"
INSERT IGNORE INTO admin_users (username, password_hash) 
VALUES ('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqSvqhuxdK');

-- ============================================
-- 第四部分：创建测试用户（可选）
-- ============================================

-- 创建一个测试用户，方便测试小程序功能
-- 手机号：13800138000
-- 注意：手机号已验证，可以直接使用
INSERT IGNORE INTO users (phone, nickname, phone_verified, is_active) 
VALUES ('13800138000', '测试用户', TRUE, TRUE);

-- ============================================
-- 初始化完成
-- ============================================

-- 验证数据是否插入成功
SELECT '========================================' AS '';
SELECT '数据库初始化完成！' AS '';
SELECT '========================================' AS '';
SELECT '' AS '';

-- 显示表统计信息
SELECT '表统计信息：' AS '';
SELECT '商品数量：', COUNT(*) FROM products;
SELECT '管理员数量：', COUNT(*) FROM admin_users;
SELECT '用户数量：', COUNT(*) FROM users;

SELECT '' AS '';
SELECT '========================================' AS '';
SELECT '默认管理员账号信息：' AS '';
SELECT '用户名：admin' AS '';
SELECT '密码：admin123' AS '';
SELECT '========================================' AS '';
SELECT '' AS '';

SELECT '测试用户信息（用于小程序测试）：' AS '';
SELECT '手机号：13800138000' AS '';
SELECT '登录验证码：查看后端控制台' AS '';
SELECT '========================================' AS '';

-- 显示所有商品列表
SELECT '' AS '';
SELECT '商品列表：' AS '';
SELECT id, name, price, stock, is_active FROM products ORDER BY id;

-- ============================================
-- 使用说明
-- ============================================
-- 
-- 1. 后台登录：
--    访问 http://localhost:5173
--    用户名：admin
--    密码：admin123
--
-- 2. 小程序测试：
--    使用手机号 13800138000 登录
--    验证码在后端控制台查看
--
-- 3. 修改管理员密码：
--    登录后台后，在"修改密码"页面修改
--
-- 4. 如需重置数据：
--    DROP DATABASE water_ordering;
--    然后重新执行此脚本
--
-- ============================================

