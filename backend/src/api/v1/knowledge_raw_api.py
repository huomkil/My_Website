from fastapi import APIRouter, HTTPException, Path, Query

from src.schemas.knowledge_raw_schemas import (
    KnowledgeRawMaterialsCreate,
    KnowledgeRawMaterialsUpdate,
    KnowledgeRawMaterialsResponse,
)
from src.servers.knowledge_raw_service import KnowledgeRawMaterialsService

router = APIRouter(prefix="/raw-materials", tags=["knowledge_raw"])
service = KnowledgeRawMaterialsService()


@router.post(
    "/",
    response_model=KnowledgeRawMaterialsResponse,
    status_code=201,
    description="创建一条新的原始素材",
    summary="创建原始素材",
)
async def create_raw_material(
    user_id: str = Query(..., description="用户 ID"),
    data: KnowledgeRawMaterialsCreate = ...,
):
    """创建原始素材"""
    return service.create(user_id, data)


@router.get(
    "/{raw_id}",
    response_model=KnowledgeRawMaterialsResponse,
    description="根据 ID 获取原始素材详情",
    summary="获取原始素材",
)
async def get_raw_material(
    user_id: str = Query(..., description="用户 ID"),
    raw_id: int = Path(..., ge=1),
):
    """根据 ID 获取原始素材"""
    raw_material = service.get_by_id(user_id, raw_id)
    if not raw_material:
        raise HTTPException(status_code=404, detail="原始素材不存在")
    return raw_material


@router.get(
    "/",
    response_model=list[KnowledgeRawMaterialsResponse],
    description="获取原始素材列表，支持分页、分类和标签筛选",
    summary="获取原始素材列表",
)
async def list_raw_materials(
    user_id: str = Query(..., description="用户 ID"),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(10, ge=1, le=100, description="返回的最大记录数"),
    category: str | None = Query(None, description="按资料分类筛选"),
    tags: str | None = Query(None, description="按标签筛选，多个标签用逗号分隔"),
):
    """获取原始素材列表"""
    tag_list = [t.strip() for t in tags.split(",") if t.strip()] if tags else None
    return service.list_all(user_id, skip, limit, category, tag_list)


@router.patch(
    "/{raw_id}",
    response_model=KnowledgeRawMaterialsResponse,
    description="根据 ID 更新原始素材，仅更新传入的字段",
    summary="更新原始素材",
)
async def update_raw_material(
    user_id: str = Query(..., description="用户 ID"),
    raw_id: int = Path(..., ge=1),
    data: KnowledgeRawMaterialsUpdate = ...,
):
    """更新原始素材"""
    raw_material = service.update(user_id, raw_id, data)
    if not raw_material:
        raise HTTPException(status_code=404, detail="原始素材不存在")
    return raw_material


@router.delete(
    "/{raw_id}",
    status_code=204,
    description="根据 ID 删除原始素材",
    summary="删除原始素材",
)
async def delete_raw_material(
    user_id: str = Query(..., description="用户 ID"),
    raw_id: int = Path(..., ge=1),
):
    """删除原始素材"""
    deleted = service.delete(user_id, raw_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="原始素材不存在")
