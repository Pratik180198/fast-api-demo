from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    return {'data': {'name': 'Pratik'}}


@app.get('/about')
def about():
    return {'data': 'about page'}


@app.get('/about/users{no}')
def users(no):
    return {'users': f'There are {no} of users'}


@app.get('/home')
def home(limit: int = 10, published: bool = False):
    if published:
        return f"This is {limit} and published is True"
    else:
        return f"This is {limit} and published is False"


