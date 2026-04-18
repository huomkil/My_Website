from sqlalchemy import Column, Integer, String
from src.db.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True) # 主键
    user_id = Column(String(36), nullable=False, unique=True, index=True) # 用户 ID，UUID 唯一且索引
    user_phone = Column(String(20), nullable=False, unique=True, index=True) # 用户手机号，唯一且索引
    user_password = Column(String(100), nullable=False) # 用户密码，存储哈希值
    user_name = Column(String(50), nullable=False, unique=True, index=True) # 用户名，唯一且索引
    user_level = Column(Integer, nullable=False, default=1) # 用户等级，默认为 1
    user_tag = Column(String(50), nullable=True) # 用户标签，逗号分隔的字符串
    user_email = Column(String(100), nullable=False, unique=True, index=True) # 用户邮箱，唯一且索引
    user_age = Column(Integer, nullable=True) # 用户年龄，允许为空
    create_time = Column(Integer, nullable=False) # 创建时间，存储 Unix 时间戳
    update_time = Column(Integer, nullable=False) # 更新时间，存储 Unix 时间戳
    is_deleted = Column(Integer, nullable=False, default=0) # 软删除标志，0 表示未删除，1 表示已删除
