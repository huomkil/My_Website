from typing import Optional, List

from sqlalchemy.orm import Session

from src.db.knowledge_raw_db.knowledge_raw_model import KnowledgeRawMaterialsModel


class KnowledgeRawMaterialsManager:
    """原始素材数据库操作层"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: str, data: dict) -> KnowledgeRawMaterialsModel:
        """创建原始素材（按用户隔离）"""
        import uuid
        raw_material = KnowledgeRawMaterialsModel(
            knowledge_raw_materials_id=str(uuid.uuid4()),
            user_id=user_id,
            **data,
        )
        self.db.add(raw_material)
        self.db.commit()
        self.db.refresh(raw_material)
        return raw_material

    def list_all(
        self,
        user_id: str,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ) -> List[KnowledgeRawMaterialsModel]:
        """获取原始素材列表（按用户隔离）"""
        query = self.db.query(KnowledgeRawMaterialsModel).filter(
            KnowledgeRawMaterialsModel.user_id == user_id
        )
        if category:
            query = query.filter(KnowledgeRawMaterialsModel.category == category)
        if tags:
            query = query.filter(KnowledgeRawMaterialsModel.tags.op("@>")(tags))
        return query.offset(skip).limit(limit).all()

    def get_by_id(self, user_id: str, raw_id: int) -> Optional[KnowledgeRawMaterialsModel]:
        """根据 ID 获取原始素材（按用户隔离）"""
        return self.db.query(KnowledgeRawMaterialsModel).filter(
            KnowledgeRawMaterialsModel.id == raw_id,
            KnowledgeRawMaterialsModel.user_id == user_id,
        ).first()

    def get_by_business_id(self, user_id: str, business_id: str) -> Optional[KnowledgeRawMaterialsModel]:
        """根据业务编号获取原始素材（按用户隔离）"""
        return self.db.query(KnowledgeRawMaterialsModel).filter(
            KnowledgeRawMaterialsModel.knowledge_raw_materials_id == business_id,
            KnowledgeRawMaterialsModel.user_id == user_id,
        ).first()

    def update(self, user_id: str, raw_id: int, data: dict) -> Optional[KnowledgeRawMaterialsModel]:
        """更新原始素材（按用户隔离）"""
        raw_material = self.get_by_id(user_id, raw_id)
        if not raw_material:
            return None
        for key, value in data.items():
            setattr(raw_material, key, value)
        self.db.commit()
        self.db.refresh(raw_material)
        return raw_material

    def delete(self, user_id: str, raw_id: int) -> bool:
        """删除原始素材（按用户隔离）"""
        raw_material = self.get_by_id(user_id, raw_id)
        if not raw_material:
            return False
        self.db.delete(raw_material)
        self.db.commit()
        return True
