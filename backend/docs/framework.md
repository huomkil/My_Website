backend/
├── src/                      # 项目源代码
│   ├── api/                  # API 路由（端点）
│   │   ├── __init__.py
│   │   ├── v1/               # 版本控制（可选）
│   │   │   ├── __init__.py
│   │   │   ├── items.py      # 示例路由文件
│   │   │   └── users.py
│   ├── core/                 # 核心配置、安全、依赖项
│   │   ├── __init__.py
│   │   ├── config.py         # Pydantic 配置模型
│   │   ├── security.py       # 认证、密码哈希等
│   │   └── dependencies.py   # 全局依赖
│   ├── models/               # 数据库模型（SQLAlchemy 或 Pydantic）
│   │   ├── __init__.py
│   │   └── item.py
│   ├── schemas/              # Pydantic 模型（请求/响应）
│   │   ├── __init__.py
│   │   └── item.py
│   ├── services/             # 业务逻辑层（可选）
│   │   ├── __init__.py
│   │   └── item_service.py
│   ├── db/                   # 数据库会话、初始化
│   │   ├── __init__.py
│   │   ├── base.py           # 基础类或导入所有模型
│   │   └── session.py        # 数据库引擎和会话
│   ├── utils/                 # 工具函数
│   │   ├── __init__.py
│   │   └── common.py
│   ├── main.py                # FastAPI 应用实例
│   └── __init__.py
├── tests/                     # 单元测试
│   ├── __init__.py
│   ├── test_api/
│   └── conftest.py            # pytest 配置
├── .env                       # 环境变量（不提交）
├── .gitignore
├── requirements.txt           # 或 pyproject.toml / poetry.lock
├── README.md
└── docker-compose.yml         # （可选，如果需要容器化）