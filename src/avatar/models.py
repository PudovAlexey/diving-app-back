from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import relationship
from src.database import Base

metadata = MetaData()


class Avatar(Base):
    __tablename__ = "avatar"
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
