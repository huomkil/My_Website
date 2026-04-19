from typing import Optional, List

from src.db.database import SessionLocal
from src.db.knowledge_raw_db import KnowledgeRawMaterialsManager
from src.schemas.knowledge_raw_schemas import (
    KnowledgeRawMaterialsCreate,
    KnowledgeRawMaterialsUpdate,
    KnowledgeRawMaterialsResponse,
)


class KnowledgeRawMaterialsService:
    """原始素材服务层 - 处理业务逻辑

    职责：
    - 管理数据库会话的开启与关闭
    - 调用 Manager 层完成 CRUD 操作
    - 将数据库模型转换为 Schema 响应对象
    - 所有操作均通过 user_id 实现用户数据隔离
    """

    def create(self, user_id: str, data: KnowledgeRawMaterialsCreate) -> KnowledgeRawMaterialsResponse:
        """创建原始素材

        Args:
            user_id: 用户 ID
            data: 创建请求体（category、title、summary、content、tags）

        Returns:
            创建成功后的原始素材响应对象
        """
        db = SessionLocal()
        try:
            manager = KnowledgeRawMaterialsManager(db)
            raw_material = manager.create(user_id, data.model_dump())
            return KnowledgeRawMaterialsResponse.model_validate(raw_material)
        finally:
            db.close()

    def get_by_id(self, user_id: str, raw_id: int) -> Optional[KnowledgeRawMaterialsResponse]:
        """根据数据库 ID 获取原始素材

        Args:
            user_id: 用户 ID（数据隔离）
            raw_id: 数据库主键 ID

        Returns:
            原始素材响应对象，不存在时返回 None
        """
        db = SessionLocal()
        try:
            manager = KnowledgeRawMaterialsManager(db)
            raw_material = manager.get_by_id(user_id, raw_id)
            if not raw_material:
                return None
            return KnowledgeRawMaterialsResponse.model_validate(raw_material)
        finally:
            db.close()

    def list_all(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> List[KnowledgeRawMaterialsResponse]:
        """获取原始素材列表

        Args:
            user_id: 用户 ID（数据隔离）
            skip: 跳过的记录数（分页）
            limit: 返回的最大记录数
            category: 按资料分类筛选
            tags: 按标签筛选（匹配包含所有指定标签的记录）

        Returns:
            原始素材响应对象列表
        """
        db = SessionLocal()
        try:
            manager = KnowledgeRawMaterialsManager(db)
            raw_materials = manager.list_all(user_id, skip, limit, category, tags)
            return [KnowledgeRawMaterialsResponse.model_validate(m) for m in raw_materials]
        finally:
            db.close()

    def update(self, user_id: str, raw_id: int, data: KnowledgeRawMaterialsUpdate) -> Optional[KnowledgeRawMaterialsResponse]:
        """更新原始素材

        Args:
            user_id: 用户 ID（数据隔离）
            raw_id: 数据库主键 ID
            data: 更新请求体（仅传入需要更新的字段）

        Returns:
            更新后的原始素材响应对象，不存在时返回 None
        """
        db = SessionLocal()
        try:
            manager = KnowledgeRawMaterialsManager(db)
            raw_material = manager.update(user_id, raw_id, data.model_dump(exclude_unset=True))
            if not raw_material:
                return None
            return KnowledgeRawMaterialsResponse.model_validate(raw_material)
        finally:
            db.close()

    def delete(self, user_id: str, raw_id: int) -> bool:
        """删除原始素材

        Args:
            user_id: 用户 ID（数据隔离）
            raw_id: 数据库主键 ID

        Returns:
            删除是否成功
        """
        db = SessionLocal()
        try:
            manager = KnowledgeRawMaterialsManager(db)
            return manager.delete(user_id, raw_id)
        finally:
            db.close()
