CREATE EXTENSION IF NOT EXISTS vector;

-- 创建 users 表
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    user_phone VARCHAR(20) NOT NULL UNIQUE,
    user_password VARCHAR(100) NOT NULL,
    user_name VARCHAR(50) NOT NULL,
    user_level INT NOT NULL DEFAULT 1,
    user_tag VARCHAR(50) DEFAULT NULL,
    user_email VARCHAR(100) DEFAULT NULL,
    user_age INT DEFAULT NULL,
    embedding VECTOR(1024) DEFAULT NULL,
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted SMALLINT NOT NULL DEFAULT 0
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_user_id ON users (user_id);
CREATE INDEX IF NOT EXISTS idx_user_phone ON users (user_phone);
CREATE INDEX IF NOT EXISTS idx_is_deleted ON users (is_deleted);
