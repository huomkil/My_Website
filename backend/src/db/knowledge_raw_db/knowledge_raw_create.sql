drop table if exists knowledge_raw_materials;
-- 创建 knowledge_raw_materials 表
CREATE TABLE IF NOT EXISTS knowledge_raw_materials (
    id SERIAL PRIMARY KEY,
    knowledge_raw_materials_id VARCHAR(36) NOT NULL,
    user_id VARCHAR(36) NOT NULL,
    category VARCHAR(100) DEFAULT NULL,
    title VARCHAR(255) DEFAULT NULL,
    summary TEXT DEFAULT NULL,
    content TEXT DEFAULT NULL,
    tags JSONB DEFAULT '[]',
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    update_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_deleted SMALLINT NOT NULL DEFAULT 0
);

-- 创建索引
CREATE INDEX IF NOT EXISTS idx_krm_business_id ON knowledge_raw_materials (knowledge_raw_materials_id);
CREATE INDEX IF NOT EXISTS idx_krm_user_id ON knowledge_raw_materials (user_id);
CREATE INDEX IF NOT EXISTS idx_krm_is_deleted ON knowledge_raw_materials (is_deleted);
