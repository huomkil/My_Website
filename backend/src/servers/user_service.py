from typing import Optional, List
from schemas.user_schemas import UserCreate, UserUpdate, UserResponse


class UserService:
    """用户服务层 - 处理业务逻辑"""

    def __init__(self):
        # 模拟数据库
        self._db: dict[int, dict] = {}
        self._next_id = 1

    def create(self, data: UserCreate) -> UserResponse:
        user = {
            "id": self._next_id,
            "username": data.username,
            "email": data.email,
            "age": data.age,
            "created_at": "2026-04-15T12:00:00",
        }
        self._db[self._next_id] = user
        self._next_id += 1
        return UserResponse(**user)

    def get_by_id(self, user_id: int) -> Optional[UserResponse]:
        user = self._db.get(user_id)
        return UserResponse(**user) if user else None

    def list_all(self, skip: int = 0, limit: int = 10) -> List[UserResponse]:
        users = list(self._db.values())[skip : skip + limit]
        return [UserResponse(**u) for u in users]

    def update(self, user_id: int, data: UserUpdate) -> Optional[UserResponse]:
        user = self._db.get(user_id)
        if not user:
            return None
        update_data = data.model_dump(exclude_unset=True)
        user.update(update_data)
        return UserResponse(**user)

    def delete(self, user_id: int) -> bool:
        return self._db.pop(user_id, None) is not None
