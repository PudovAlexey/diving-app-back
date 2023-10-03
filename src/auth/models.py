from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column, JSON, Boolean
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base
from src.userInfo.models import UserInfo


metadata = MetaData()


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    Permissions = Column(JSON)


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey(Role.id))
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    user_info_id = Column(Integer, ForeignKey(UserInfo.id))
    user_info = relationship(UserInfo)