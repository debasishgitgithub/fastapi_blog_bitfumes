from typing import List
from pydantic import BaseModel


class Blog(BaseModel):
    name: str
    desc : str | None = None
    class Config():
        from_attributes = True


class BaseShowBlog(Blog):
    id: int

class User(BaseModel):
    name: str
    email:str
    password: str
    class Config():
        from_attributes = True

class BaseShowUser(BaseModel):
    id: int
    name:str
    email: str
    class Config():
        from_attributes = True
        
class ShowUser(BaseShowUser):
    blogs: List[BaseShowBlog] =[]


# class ShowBlog(Blog):
#     name: str
#     desc : str | None = None
class ShowBlog(BaseShowBlog):
    creator: BaseShowUser
    
class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
