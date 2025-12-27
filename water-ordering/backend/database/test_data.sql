-- ============================================
-- 测试数据（可选）
-- ============================================
-- 说明：此文件包含测试商品数据，用于开发和测试
-- 执行方式：在创建表后执行，可以多次执行（会跳过已存在的商品）
-- ============================================

-- 插入测试商品数据
-- 注意：如果商品名称已存在，不会重复插入（使用 INSERT IGNORE）
INSERT IGNORE INTO products (name, description, price, image_url, stock, is_active) VALUES
('18.9L 桶装水', '优质纯净水，适合家庭和办公室使用', 15.00, '', 100, TRUE),
('12L 桶装水', '小容量桶装水，适合小家庭使用', 12.00, 'https://via.placeholder.com/300x300?text=12L+桶装水', 80, TRUE),
('5L 桶装水', '便携式小桶装水，方便携带', 8.00, 'https://via.placeholder.com/300x300?text=5L+桶装水', 150, TRUE),
('矿泉水 24瓶装', '500ml 瓶装矿泉水，24瓶一箱', 35.00, 'https://via.placeholder.com/300x300?text=矿泉水+24瓶装', 200, TRUE),
('纯净水 12瓶装', '550ml 瓶装纯净水，12瓶一箱', 20.00, 'https://via.placeholder.com/300x300?text=纯净水+12瓶装', 180, TRUE),
('高端矿泉水 6瓶装', '1L 高端矿泉水，6瓶装，适合商务场合', 88.00, 'https://via.placeholder.com/300x300?text=高端矿泉水', 50, TRUE),
('苏打水 12瓶装', '500ml 苏打水，12瓶装，清爽口感', 28.00, 'https://via.placeholder.com/300x300?text=苏打水+12瓶装', 120, TRUE),
('运动饮料 24瓶装', '500ml 运动饮料，24瓶装，补充电解质', 45.00, 'https://via.placeholder.com/300x300?text=运动饮料', 100, TRUE);

-- 注意：如果商品名称已存在，不会重复插入
-- 如果需要清空测试数据，执行：
-- DELETE FROM products;

