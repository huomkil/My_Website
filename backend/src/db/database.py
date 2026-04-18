from pydantic_settings import BaseSettings
from pydantic import ConfigDict

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv(".env")

class DBSettings(BaseSettings):
    # 让 Pydantic 自动从环境变量读取，不要手动调用 getenv()
    mysql_host: str = "localhost"  # 可以设置默认值
    mysql_port: int = 3306
    mysql_user: str = "root"
    mysql_root_password: str = ""
    mysql_database: str = "mydb"

    @property
    def database_url(self) -> str:
        return (
            f"mysql+pymysql://{self.mysql_user}:{self.mysql_root_password}"
            f"@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"
        )

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # 忽略 .env 中未在此类中定义的字段
    )

settings = DBSettings()

# 可选：验证配置是否完整
if not settings.mysql_host or not settings.mysql_root_password:
    raise ValueError("数据库配置不完整，请检查 .env 文件")

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,  # 设为 True 可查看 SQL 日志
)

# 定义 Base 类，所有模型都将继承它
Base = declarative_base()
# 创建数据库会话工厂,每次需要数据库操作时都可以创建一个新的会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)