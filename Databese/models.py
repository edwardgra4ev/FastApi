from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from Databese.database import Base
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
import datetime


# Таблица users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    key = relationship("UserKey", back_populates="owner")


# Таблица user_key
class UserKey(Base):
    __tablename__ = "user_key"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(UUID(as_uuid=True), default=uuid4)
    owner_id = Column(Integer, ForeignKey("users.id"))
    datetime_creation = Column(DateTime, default=datetime.datetime.utcnow)
    owner = relationship("User", back_populates="key")