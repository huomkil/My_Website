from typing import Optional, List

from src.db.database import SessionLocal
from src.db.user_db import UserManager
from src.schemas.user_schemas import UserCreate, UserUpdate, UserResponse


class UserService:
    """用户服务层 - 处理业务逻辑"""

    def create(self, data: UserCreate) -> UserResponse:
        """创建用户"""
        db = SessionLocal()
        try:
            manager = UserManager(db)
            user = manager.create(data)
            return UserResponse.model_validate(user)
        finally:
            db.close()

    def get_by_id(self, user_id: int) -> Optional[UserResponse]:
        """根据 ID 获取用户"""
        db = SessionLocal()
        try:
            manager = UserManager(db)
            user = manager.get_by_id(user_id)
            if not user:
                return None
            return UserResponse.model_validate(user)
        finally:
            db.close()

    def list_all(self, skip: int = 0, limit: int = 10) -> List[UserResponse]:
        """获取用户列表"""
        db = SessionLocal()
        try:
            manager = UserManager(db)
            users = manager.list_all(skip, limit)
            return [UserResponse.model_validate(u) for u in users]
        finally:
            db.close()

    def update(self, user_id: int, data: UserUpdate) -> Optional[UserResponse]:
        """更新用户信息"""
        db = SessionLocal()
        try:
            manager = UserManager(db)
            user = manager.update(user_id, data)
            if not user:
                return None
            return UserResponse.model_validate(user)
        finally:
            db.close()

    def delete(self, user_id: int) -> bool:
        """删除用户"""
        db = SessionLocal()
        try:
            manager = UserManager(db)
            return manager.delete(user_id)
        finally:
            db.close()
