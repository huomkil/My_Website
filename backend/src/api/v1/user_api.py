from fastapi import APIRouter, HTTPException, Path

from src.schemas.user import UserCreate, UserUpdate, UserResponse
from src.servers.user_service import UserService

router = APIRouter(prefix="/users", tags=["user"])
service = UserService()


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(data: UserCreate):
    """创建用户"""
    return service.create(data)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int = Path(..., ge=1)):
    """根据 ID 获取用户"""
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.get("/", response_model=list[UserResponse])
async def list_users(skip: int = 0, limit: int = 10):
    """获取用户列表"""
    return service.list_all(skip, limit)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int = Path(..., ge=1),
    data: UserUpdate = ...,
):
    """更新用户信息"""
    user = service.update(user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int = Path(..., ge=1)):
    """删除用户"""
    deleted = service.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="用户不存在")
