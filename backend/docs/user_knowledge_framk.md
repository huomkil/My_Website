# 用户知识库设计

## 1. 概述

用户知识库是个人知识管理系统的数据存储与关系组织模块，用于将用户的原始素材提炼为结构化知识，并建立知识之间的关联。

### 1.1 设计目标

- **知识存储**：持久化保存用户上传的原始素材和提炼的知识点
- **语义搜索**：通过向量相似度实现基于含义的内容检索
- **关系追溯**：记录知识点与原始素材的衍生关系，支持完整知识链路追溯
- **架构简洁**：以 PostgreSQL 为核心，一库搞定关系存储与向量搜索

### 1.2 技术栈

| 组件 | 选型 | 说明 |
|------|------|------|
| 数据库 | PostgreSQL + pgvector | 关系存储 + 原生向量搜索 |
| 对象存储 | MinIO / S3 | 原始文件存储 |
| 向量模型 | OpenAI / BGE / M3E | 文本向量化 |

## 2. 核心设计思路

### 2.1 三层逻辑概念

知识库系统分为三个逻辑层次：

| 层次 | 说明 | 节点类型 |
|------|------|----------|
| 原始库 | 存放用户上传的原始素材（文件、网页、录音等） | `raw` |
| 知识库 | 存放从原始素材中提炼的知识点 | `refined` |
| 节点库 | 存放知识点之间的关系连接 | 通过 knowledge_edges 表实现 |

### 2.2 物理存储

逻辑上的三层概念在物理上通过 **三张表** 实现：

```
knowledge_raw_materials  ── 原始素材表，存放用户录入的 Markdown 内容
knowledge_nodes          ── 知识节点表，存放提炼的知识点
knowledge_edges          ── 关系表，独立存储节点之间的关系连接
```

这种设计的优势：
- **职责清晰**：原始素材、提炼知识、关系连接各自独立，表结构更专注
- **查询高效**：原始素材与知识数据物理隔离，查询互不干扰
- **可追溯**：通过 `raw_id` 字段记录来源，支持完整链路追溯
- **可扩展**：`JSONB` 属性字段支持动态扩展，关系类型可随时新增

## 3. 数据库设计

### 3.1 原始素材表（knowledge_raw_materials）

存放用户录入的原始 Markdown 内容。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | ID | 主键 |
| knowledge_raw_materials_id | UUID | 业务编号，唯一标识 |
| user_id | UUID | 所属用户 ID |
| category | VARCHAR | 资料分类 |
| title | VARCHAR | 标题 |
| summary | TEXT | 简介 |
| content | TEXT | Markdown 正文内容 |
| tags | JSONB | 标签数组，如 `["标签1", "标签2"]` |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### 3.2 知识节点表（knowledge_nodes）

存放从原始素材中提炼的知识点。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| user_id | UUID | 所属用户 ID |
| title | VARCHAR | 节点标题 |
| content | TEXT | 正文内容 |
| raw_id | UUID | 来源原始素材 ID，外键关联 knowledge_raw_materials.id（可为空） |
| embedding | vector(1536) | 向量字段，用于语义搜索 |
| properties | JSONB | 动态扩展属性 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

### 3.3 关系表（knowledge_edges）

独立存储知识节点之间的关系连接。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| source_id | UUID | 源节点 ID，外键关联 knowledge_nodes.id |
| target_id | UUID | 目标节点 ID，外键关联 knowledge_nodes.id |
| relation_type | VARCHAR | 关系类型（见下表） |
| properties | JSONB | 关系扩展属性 |
| created_at | TIMESTAMP | 创建时间 |

#### 关系类型

| 类型 | 说明 | 示例 |
|------|------|------|
| `references` | 引用 | 知识点 A 引用了知识点 B |
| `contains` | 包含 | 知识模块 A 包含子知识点 B |
| `derives` | 衍生 | 提炼节点 B 衍生自原始节点 A |
| `compares` | 对比 | 知识点 A 与知识点 B 存在对比关系 |
| `supplements` | 补充 | 知识点 B 是对知识点 A 的补充 |

## 4. 向量与语义搜索（pgvector）

### 4.1 核心概念

- **向量**：将文本通过 AI 模型转换成的数字数组（如 1536 维）
- **相似度**：通过计算向量之间的距离衡量文本语义相似度
- **语义搜索**：不依赖关键词匹配，而是查找含义相近的内容

### 4.2 向量搜索示例

语义搜索查询知识节点：

```sql
SELECT id, title, content
FROM knowledge_nodes
ORDER BY embedding <=> 'query_vector_here'
LIMIT 10;
```

### 4.3 索引选择

| 索引类型 | 特点 | 适用场景 |
|----------|------|----------|
| HNSW | 查询速度快，精度高 | 推荐首选，适合大多数场景 |
| IVFFlat | 创建速度快，内存占用低 | 超大数据量时考虑 |

## 5. 数据流转

### 5.1 上传原始素材

```
用户录入 Markdown 内容
    ├── 1. 写入 knowledge_raw_materials 表（title、summary、content、tags）
    └── 2. 异步任务：
            └── 生成文本向量 → embedding（写入关联的 knowledge_nodes）
```

### 5.2 提炼知识点

```
用户提炼知识点
    ├── 1. 创建 knowledge_nodes 记录（填写 title、content）
    ├── 2. raw_id 指向来源的原始素材（knowledge_raw_materials.id，可为空）
    ├── 3. 对提炼内容生成向量 → embedding
    └── 4. 可选：建立与相关知识点的关系（写入 knowledge_edges）
```

### 5.3 建立知识关系

```
用户建立关系
    └── 写入 knowledge_edges 表（source_id → target_id + relation_type）
```

## 6. 查询场景

### 6.1 语义搜索

查找与查询内容语义最相似的知识点。

```sql
SELECT id, title, content
FROM knowledge_nodes
ORDER BY embedding <=> 'query_vector'
LIMIT 10;
```

### 6.2 查找原始素材的提炼结果

给定一个原始素材，找到所有从它提炼出来的知识点。

```sql
SELECT id, title, content
FROM knowledge_nodes
WHERE raw_id = 'raw-material-uuid';
```

### 6.3 查找知识点的所有关联

找到与指定节点有连接关系的所有节点。

```sql
-- 作为源节点的关系
SELECT n.id, n.title, n.content, e.relation_type
FROM knowledge_edges e
JOIN knowledge_nodes n ON n.id = e.target_id
WHERE e.source_id = 'target-node-uuid'

UNION

-- 作为目标节点的关系
SELECT n.id, n.title, n.content, e.relation_type
FROM knowledge_edges e
JOIN knowledge_nodes n ON n.id = e.source_id
WHERE e.target_id = 'target-node-uuid';
```

### 6.4 完整知识链路追溯

从原始素材出发，追溯其提炼结果和关联关系。

```
原始素材（knowledge_raw_materials）
    └── raw_id 关联 → 提炼节点（knowledge_nodes）
            └── knowledge_edges 关联 → 其他知识节点
```

## 7. 设计优势总结

| 优势 | 说明 |
|------|------|
| 职责清晰 | 原始素材、知识节点、关系连接三表独立，结构更专注 |
| 查询高效 | 查询知识节点无需过滤类型，原始素材与知识数据物理隔离 |
| 可追溯 | `raw_id` 外键关联，支持从原始素材到知识节点的完整链路回溯 |
| 可扩展 | `JSONB` 属性字段支持动态扩展，关系类型可随时新增 |
| 语义搜索 | pgvector 原生向量搜索，知识节点支持语义检索 |
| 架构简洁 | PostgreSQL 一库搞定，降低运维复杂度 |
