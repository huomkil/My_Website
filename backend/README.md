# 我的专属网站 - 后端服务

## 编程原则

1. 先确定总需求框架
2. 再确定数据格式
3. 然后快速开发实现功能
4. 再评估功能
5. 最后再单独优化

## 项目简介

本项目是一个个人知识管理系统，用于：

- **知识存储**：将个人知识和经验存入数据库持久化保存
- **知识查询**：方便查询和检索所需知识
- **文档生成**：自动生成文档，便于自我提升和快速匹配适合的工作机会

### 为什么不用 NotebookLM 等现有工具？

| 对比项 | NotebookLM 等 | 本项目 |
|--------|--------------|--------|
| 部署方式 | 云端服务 | 本地运行 |
| 模型选择 | 固定 | 可自由切换大模型 |
| 定制化 | 有限 | 完全按照个人需求修改 |
| 响应速度 | 受网络影响 | 本地直接调用，速度快 |
| 社区化 | 通用 | 个性化社区，适合个人使用场景 |

## 技术栈

- **Python** >= 3.9
- **FastAPI** >= 0.115.0 — Web 框架
- **SQLAlchemy** >= 2.0.0 — ORM 数据库操作
- **Pydantic Settings** >= 2.0.0 — 配置管理
- **MySQL** 8.0 — 关系型数据库
- **Redis** 7 — 缓存服务
- **uv** — Python 包管理器
- **Docker Compose** — 容器化部署

## 项目结构

```
backend/
├── src/                      # 项目源代码
│   ├── api/                  # API 路由层
│   │   └── v1/               # API v1 版本
│   │       └── user_api.py   # 用户相关接口
│   ├── core/                 # 核心配置与工具
│   ├── db/                   # 数据库配置
│   │   └── aa.py             # 数据库连接与会话
│   ├── langchain_workflow/   # LangChain 工作流
│   ├── models/               # 数据模型
│   ├── routes/               # 路由聚合
│   ├── schemas/              # 请求/响应 Schema
│   │   └── user_schemas.py   # 用户数据模型
│   ├── servers/              # 业务逻辑层
│   │   └── user_service.py   # 用户服务
│   ├── utils/                # 工具函数
│   ├── main.py               # FastAPI 应用入口
│   └── __init__.py
├── tests/                    # 单元测试
├── docs/                     # 项目文档
│   └── framework.md          # 框架设计文档
├── .env                      # 环境变量（不提交）
├── .env.example              # 环境变量模板（提交）
├── docker-compose.yml        # Docker 编排配置
├── pyproject.toml            # 项目依赖与构建配置
├── uv.lock                   # uv 锁定文件
└── README.md
```

## 快速开始

### 环境要求

- Python 3.9+
- uv 包管理器
- Docker & Docker Compose（可选，用于数据库服务）

### 安装依赖

```bash
# 使用 uv 安装项目依赖
uv sync

# 安装开发依赖（含 pytest, black, ruff, mypy）
uv sync --all-extras
```

### 环境变量配置

复制 `.env.example` 文件并修改配置：

```bash
cp .env.example .env
```

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `MYSQL_DATABASE` | 数据库名称 | `my_website` |
| `MYSQL_USER` | 数据库用户 | `root` |
| `MYSQL_ROOT_PASSWORD` | 数据库密码 | 自行设置 |
| `MYSQL_PORT` | MySQL 端口 | `3306` |
| `MYSQL_DATA_PATH` | MySQL 数据持久化路径 | 本地路径 |
| `REDIS_PORT` | Redis 端口 | `6379` |
| `REDIS_DATA_PATH` | Redis 数据持久化路径 | 本地路径 |

### 启动服务

#### 方式一：直接启动

```bash
uv run python -m uvicorn src.main:app --reload
```

服务启动后访问：
- API 根路径：http://127.0.0.1:8000/
- API 文档（自动）：http://127.0.0.1:8000/docs
- API 文档（ReDoc）：http://127.0.0.1:8000/redoc

#### 方式二：Docker Compose 启动（推荐，用于数据库服务）

```bash
# 启动 MySQL 和 Redis 服务
docker compose up -d

# 查看服务状态
docker compose ps

# 停止服务
docker compose down
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 返回请求信息（URL、方法、头部、查询参数等） |
| GET | `/u` | 返回请求头中的 `u` 字段 |
| GET | `/user/{user}` | 返回指定用户 ID |
| GET | `/user` | 分页查询用户列表（参数：`page`, `size`） |

### 用户管理接口（`/api/v1/users`）

| 方法 | 路径 | 说明 | 请求体 |
|------|------|------|--------|
| POST | `/api/v1/users/` | 创建用户 | `UserCreate`（username, email, age?） |
| GET | `/api/v1/users/{user_id}` | 获取用户 | — |
| GET | `/api/v1/users/` | 用户列表（参数：`skip`, `limit`） | — |
| PATCH | `/api/v1/users/{user_id}` | 更新用户 | `UserUpdate`（username?, email?, age?） |
| DELETE | `/api/v1/users/{user_id}` | 删除用户 | — |

## 系统规划

### 用户系统

用于用户登录和数据隔离，确保不同用户的数据相互独立。

- [x] 用户创建、获取、更新、删除接口（`/api/v1/users`）
- [ ] 用户认证与登录
- [ ] 数据隔离

### 知识库系统

用于存储和管理个人知识库数据。

#### 知识库结构

知识库采用类似 skill 的消息元结构，使用单词硬匹配方式组织。

```
skill-name/
├── SKILL.md          # 必需：核心指令与元数据
├── scripts/          # 可选：可执行脚本 (Python/Bash)
├── references/       # 可选：参考文档、API 说明、最佳实践
└── assets/           # 可选：模板、图片等静态资源
```

#### 知识库分类

| 类型 | 说明 |
|------|------|
| **skill** | 技能配置，记录用户和通用的 skill，用于对话时从笔记中获取处理能力（如生成简历、规划任务等） |
| **study-note** | 学习笔记，记录个人学习过程和心得 |
| **depend-note** | 收集笔记，记录参考过的知识来源和资料 |

### 智能体系统

（规划中）基于知识库构建智能体，实现自动化知识处理。

## 开发规范

### 代码格式化

```bash
# 使用 black 格式化代码
uv run black src/

# 使用 ruff 检查代码风格
uv run ruff check src/
```

### 类型检查

```bash
# 使用 mypy 进行类型检查
uv run mypy src/
```

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行测试并生成覆盖率报告
uv run pytest --cov=src
```

## 许可证

本项目为个人使用，保留所有权利。
