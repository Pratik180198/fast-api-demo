from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn

app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': 'Pratik'}}


@app.get('/about')
def about():
    return {'data': 'about page'}


@app.get('/about/users{no}')
def users(no:int):
    return {'users': f'There are {no} of users'}


@app.get('/home')
def home(limit: int = 10, published: bool = False):
    if published:
        return f"This is {limit} and published is True"
    else:
        return f"This is {limit} and published is False"


class Define(BaseModel):
    name: str
    published: Optional[bool]
    age: int


@app.post('/request')
def get_data(blog: Define):
    return f"This is {blog.name} and his age is {blog.age}"


if __name__ == '__main__':
    uvicorn.run(app, host = "127.0.0.1", port = 9000)
