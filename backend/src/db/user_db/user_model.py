from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from pgvector.sqlalchemy import Vector
from src.db.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键
    user_id = Column(String(36), nullable=False, index=True)  # 用户 ID，UUID，索引
    user_phone = Column(String(20), nullable=False, unique=True, index=True)  # 用户手机号，唯一且索引
    user_password = Column(String(100), nullable=False)  # 用户密码，存储哈希值
    user_name = Column(String(50), nullable=False, index=True)  # 用户名
    user_level = Column(Integer, nullable=False, default=1)  # 用户等级，默认为 1
    user_tag = Column(String(50), nullable=True)  # 用户标签，逗号分隔的字符串
    user_email = Column(String(100), nullable=True, index=True)  # 用户邮箱
    user_age = Column(Integer, nullable=True)  # 用户年龄，允许为空
    embedding = Column(Vector(1024), nullable=True)  # 向量嵌入，用于语义搜索
    create_time = Column(TIMESTAMP, nullable=False, server_default=func.now())  # 创建时间
    update_time = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())  # 更新时间
    is_deleted = Column(Integer, nullable=False, default=0)  # 软删除标志，0 表示未删除，1 表示已删除
