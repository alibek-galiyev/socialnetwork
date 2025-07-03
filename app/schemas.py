from pydantic import BaseModel, EmailStr, conint
from typing import Optional, Union
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    nickname: Optional[str] = "Anonymous"
    password: str

    model_config = {"from_attributes": True}

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    nickname: Optional[str] = "Anonymous"

    model_config = {"from_attributes": True}


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    model_config = {"from_attributes": True}
    

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)

    model_config = {"from_attributes": True}


class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    owner_id: Optional[int] = None
    


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
    owner_id: Optional[int] = None
    owner: UserResponse
    
    model_config = {"from_attributes": True}


class PostVoteResponse(BaseModel):
    Post: PostResponse
    votes: int

    model_config = {"from_attributes": True}



class Token(BaseModel):
    access_token: str
    token_type: str

    model_config = {"from_attributes": True}


class TokenData(BaseModel):
    id: Union[int, str]

    model_config = {"from_attributes": True}


