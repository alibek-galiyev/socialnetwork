from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


class CreatePost(Post):
    created_at: Optional[datetime] = None


class UpdatePost(Post):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = True
    rating: Optional[int] = None

    model_config = {"from_attributes": True}


class PostResponse(BaseModel):
    title: str
    content: str
    published: bool

    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    email: EmailStr
    password: str

    model_config = {"from_attributes": True}

class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = {"from_attributes": True}