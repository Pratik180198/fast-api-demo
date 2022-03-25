from pydantic import BaseModel
from typing import List


class BaseBlog(BaseModel):
    blog: str
    body: str


class Blog(BaseBlog):
    class Config:
        orm_mode = True


class ShowUser(BaseModel):
    username: str
    email: str
    blogs: List[Blog] = []

    class Config:
        orm_mode = True


class ShowBlog(BaseModel):
    blog: str
    body: str
    creator: ShowUser

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    email: str
    password: str



