from fastapi import APIRouter

from src.api.v1.user_api import router as user_router

# 路由总入口
router = APIRouter(prefix="/api/v1")

# 注册各业务路由
router.include_router(user_router)
