from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class KnowledgeRawMaterialsCreate(BaseModel):
    category: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = []


class KnowledgeRawMaterialsUpdate(BaseModel):
    category: Optional[str] = None
    title: Optional[str] = None
    summary: Optional[str] = None
    content: Optional[str] = None
    tags: Optional[List[str]] = None


class KnowledgeRawMaterialsResponse(BaseModel):
    id: int
    knowledge_raw_materials_id: str
    user_id: str
    category: Optional[str]
    title: Optional[str]
    summary: Optional[str]
    content: Optional[str]
    tags: Optional[List[str]]
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True
