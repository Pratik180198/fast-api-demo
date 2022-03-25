import models
import schemas
from typing import List
from database import engine, SessionLocal
from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from Hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/add_details', status_code=status.HTTP_201_CREATED, tags=['Blog'])
def add_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.BlogTable(blog=request.blog, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/get_details', tags=['Blog'], response_model=List[schemas.ShowBlog])
def get_details(db: Session = Depends(get_db)):
    get_data = db.query(models.BlogTable).all()
    return get_data


@app.get('/get_details_by_id/{id1}', response_model=schemas.ShowBlog, status_code=200, tags=['Blog'])
def get_by_id(id1, response: Response, db: Session = Depends(get_db)):
    id_details = db.query(models.BlogTable).filter(models.BlogTable.id == id1).first()
    if not id_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id: {id1} is not found.")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return f"The id: {id} is not found."

    return id_details


@app.delete('/delete_by_id/{id1}', status_code=status.HTTP_201_CREATED, tags=['Blog'])
def delete_by_id(id1, db: Session = Depends(get_db)):
    delete_id = db.query(models.BlogTable).filter(models.BlogTable.id == id1)
    if not delete_id.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This id {id1} is not present")
    delete_id.delete(synchronize_session=False)
    db.commit()
    return "Deleted"


@app.put('/update/{id1}', status_code=status.HTTP_202_ACCEPTED, tags=['Blog'])
def update(id1, request: schemas.Blog, db: Session = Depends(get_db)):
    update_username = db.query(models.BlogTable).filter(models.BlogTable.id == id1)
    if not update_username.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"This id {id1} is not present")
    update_username.update({'blog': request.blog})
    db.commit()
    return "updated"


@app.post('/create_user', tags=['User'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    add_user = models.UserTable(username=request.username, email=request.email,
                                password=Hash.bcrpyt(request.password))
    db.add(add_user)
    db.commit()
    db.refresh(add_user)
    return "User added"


@app.get('/show_user', response_model=List[schemas.ShowUser], tags=['User'])
def show_user(db: Session = Depends(get_db)):
    show_data = db.query(models.UserTable).all()
    return show_data
