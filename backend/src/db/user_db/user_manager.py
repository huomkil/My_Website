from typing import Optional, List

from sqlalchemy.orm import Session

from src.db.user_db.user_model import UserModel
from src.schemas.user_schemas import UserCreate, UserUpdate


class UserManager:
    """用户数据库操作层"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: UserCreate) -> UserModel:
        """创建用户"""
        import uuid
        if self.db.query(UserModel).filter(UserModel.user_phone == data.user_phone).first():
            raise ValueError("User ID already exists")

        user = UserModel(
            user_id=str(uuid.uuid4()),
            **data.model_dump(),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def list_all(self, skip: int = 0, limit: int = 10) -> List[UserModel]:
        """获取用户列表"""
        return self.db.query(UserModel).offset(skip).limit(limit).all()

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        """根据 ID 获取用户"""
        return self.db.query(UserModel).filter(UserModel.id == user_id).first()

    def update(self, user_id: int, data: UserUpdate) -> Optional[UserModel]:
        """更新用户信息"""
        user = self.get_by_id(user_id)
        if not user:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        """删除用户"""
        user = self.get_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
