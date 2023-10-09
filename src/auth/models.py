from enum import Enum
from sqlalchemy import MetaData, Integer, String, TIMESTAMP, ForeignKey, Table, Column, JSON, Boolean, Enum as AlchemyEnum
from sqlalchemy.dialects.postgresql import ENUM as pgEnum
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import relationship
from datetime import datetime
from src.database import Base, engine
from src.userInfo.models import UserInfo


metadata = MetaData()


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    Permissions = Column(JSON)

class GenderEnum(Enum):
    MALE = 'male'
    FEMALE = 'female'


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    patronymic = Column(String)
    username = Column(String, nullable=False)
    birth_date = Column(TIMESTAMP, nullable=False)
    gender = Column(AlchemyEnum(GenderEnum))
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey(Role.id))
    email: str = Column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    user_info_id = Column(Integer, ForeignKey(UserInfo.id))
    user_info = relationship(UserInfo)