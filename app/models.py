from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, text, ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    published = Column(Boolean, server_default="true", nullable=False)
    created_at = Column(DateTime, server_default=text("now()"), nullable=False)
    rating = Column(Integer, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    nickname = Column(String, unique=False, nullable=False, default="Anonymous")
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=text("now()"), nullable=False)
    is_active = Column(Boolean, server_default="true", nullable=False)



class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)

    post = relationship("Post")
    user = relationship("User")