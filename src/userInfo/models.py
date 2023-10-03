from sqlalchemy import Column, Integer, String, MetaData, ForeignKey
from src.database import Base
from sqlalchemy.orm import validates, relationship
from src.avatar.models import Avatar

metadata = MetaData()


class UserInfo(Base):
    __tablename__ = "user_info"
    id = Column(Integer, primary_key=True, index=True)
    avatar_id = Column(Integer, ForeignKey(Avatar.id))
    about = Column(String, nullable=True)
    experience = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)
    # user_id = Column(Integer, ForeignKey(User.id))
    # user = relationship('User', backref='user_info')

    @validates('rating')
    def validate_value(self, key, value):
        if value is None or 0 <= value <= 5:
            return value
        raise ValueError("Значение должно быть от 0 до 5")
