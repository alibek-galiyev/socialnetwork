from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, text


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, server_default="true", nullable=False)
    created_at = Column(DateTime, server_default=text("now()"), nullable=False)
    rating = Column(Integer, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=text("now()"), nullable=False)
    is_active = Column(Boolean, server_default="true", nullable=False)