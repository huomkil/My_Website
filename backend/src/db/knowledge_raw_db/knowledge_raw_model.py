from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from src.db.database import Base


class KnowledgeRawMaterialsModel(Base):
    __tablename__ = "knowledge_raw_materials"

    id = Column(Integer, primary_key=True, autoincrement=True)
    knowledge_raw_materials_id = Column(String(36), nullable=False, unique=True, index=True)
    user_id = Column(String(36), nullable=False, index=True)
    category = Column(String(100), nullable=True)
    title = Column(String(255), nullable=True)
    summary = Column(Text, nullable=True)
    content = Column(Text, nullable=True)
    tags = Column(JSONB, nullable=True, default=list)
    create_time = Column(TIMESTAMP, nullable=False, server_default=func.now())
    update_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    is_deleted = Column(Integer, nullable=False, default=0)
