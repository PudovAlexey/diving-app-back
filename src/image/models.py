from sqlalchemy import Column, Integer, String, MetaData
from src.database import Base

metadata = MetaData()

class Image(Base):
  __tablename__ = "image"
  id = Column(Integer, primary_key=True, index=True)
  path = Column(String, nullable=False)
  name = Column(String, nullable=False)
  description = Column(String, nullable=False)
