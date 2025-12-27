-- ============================================
-- 修复数据库字段：添加 phone_verified 字段
-- ============================================
-- 说明：如果 users 表中缺少 phone_verified 字段，执行此脚本
-- 如果字段已存在会报错，可以忽略

ALTER TABLE users 
ADD COLUMN IF NOT EXISTS phone_verified BOOLEAN DEFAULT FALSE COMMENT '手机号是否已验证';

-- ============================================
-- 修复数据库字段：修改 openid 允许为 NULL
-- ============================================
-- 说明：如果 users 表中的 openid 字段不允许为 NULL，执行此脚本

ALTER TABLE users 
MODIFY COLUMN openid VARCHAR(100) NULL COMMENT '微信 openid（可选）';

