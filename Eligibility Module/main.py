from fastapi import FastAPI, Depends, status, HTTPException, Request, File, UploadFile
import pandas as pd
from database import engine, get_db
import models
from schemas import UserDetails, Stage, StageTwo
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()

templates = Jinja2Templates(directory="templates/")

models.Base.metadata.create_all(bind=engine)


@app.get('/uploadcsv', response_class=HTMLResponse)
def read(request: Request):
    return templates.TemplateResponse("csv.html", {"request": request})


@app.post('/submitcsv')
def handle_csv(csvfile: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(csvfile.file)
        for index, row in df.iterrows():
            if db.query(models.StudentTable).filter(models.StudentTable.email_id == row.email_id).first():
                pass
            else:
                engine.execute(
                    "INSERT INTO "
                    "demo_fastapi.students(full_name,email_id,graduation_completed,stream,cgpa,entrance_exam_score)"
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    row.full_name, row.email_id, row.graduation_completed, row.stream, row.cgpa,
                    row.entrance_exam_score)
        return "Sucessfully added"
    except Exception as e:
        return e


@app.get('/add_details', response_class=HTMLResponse)
def read(request: Request):
    return templates.TemplateResponse("add_details.html", {"request": request})


@app.post('/add_details', status_code=status.HTTP_201_CREATED, response_class=HTMLResponse)
def add_details(request: Request, form_data: UserDetails = Depends(UserDetails.as_form), db: Session = Depends(get_db)):
    new_details = models.StudentTable(full_name=form_data.full_name,
                                      email_id=form_data.email_id,
                                      graduation_completed=form_data.graduation_completed,
                                      stream=form_data.stream, cgpa=form_data.cgpa,
                                      entrance_exam_score=form_data.entrance_exam_score)
    db.add(new_details)
    db.commit()
    db.refresh(new_details)
    return templates.TemplateResponse("add_details.html", {"request": request})


@app.get('/get_details')
def get_details(db: Session = Depends(get_db)):
    get_data = db.query(models.StudentTable).all()
    return get_data


@app.get('/stage_one', response_class=HTMLResponse)
def read_stage_one(request: Request):
    return templates.TemplateResponse("stage_one.html", {"request": request})


@app.post('/stage_one')
def grad_complete(request: Request, form_details: Stage = Depends(Stage.as_form), db: Session = Depends(get_db)):
    try:
        if form_details.graduation_completed == 'both':
            details = db.query(models.StudentTable).filter(
                models.StudentTable.graduation_completed.in_(['yes', 'no'])).all()

            db.query(models.Stages).delete()
            db.commit()

            for detail in details:

                if db.query(models.Stages).filter(models.Stages.email_id == detail.email_id).first():
                    pass
                else:
                    new_details = models.Stages(id=detail.id,
                                                full_name=detail.full_name,
                                                email_id=detail.email_id,
                                                graduation_completed=detail.graduation_completed,
                                                stream=detail.stream, cgpa=detail.cgpa,
                                                entrance_exam_score=detail.entrance_exam_score)

                    db.add(new_details)
                    db.commit()
                    db.refresh(new_details)

            return templates.TemplateResponse("stage_one.html", {"request": request, "details": details})

        details = db.query(models.StudentTable).filter(
            models.StudentTable.graduation_completed == form_details.graduation_completed).all()
        if not details:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'That type of data is not present')

        db.query(models.Stages).delete()
        db.commit()
        for detail in details:
            if db.query(models.Stages).filter(models.Stages.email_id == detail.email_id).first():
                pass
            else:
                new_details = models.Stages(id=detail.id,
                                            full_name=detail.full_name,
                                            email_id=detail.email_id,
                                            graduation_completed=detail.graduation_completed,
                                            stream=detail.stream, cgpa=detail.cgpa,
                                            entrance_exam_score=detail.entrance_exam_score)

                db.add(new_details)
                db.commit()
                db.refresh(new_details)

        return templates.TemplateResponse("stage_one.html", {"request": request, "details": details})

    except HTTPException as e:
        return e


@app.get('/stage_two', response_class=HTMLResponse)
def read_stage_two(request: Request):
    return templates.TemplateResponse("two.html", {"request": request})


@app.post('/stagetwo')
def check_stream(request: Request, form_details: StageTwo = Depends(StageTwo.as_form), db: Session = Depends(get_db)):
    # print(form_details.stream)
    details = db.query(models.Stages).filter(models.Stages.stream.in_(form_details.stream)).all()
    db.query(models.StageTwo).delete()
    db.commit()

    for detail in details:
        if db.query(models.StageTwo).filter(models.StageTwo.email_id == detail.email_id).first():
            pass
        else:
            new_details = models.StageTwo(id=detail.id,
                                          full_name=detail.full_name,
                                          email_id=detail.email_id,
                                          graduation_completed=detail.graduation_completed,
                                          stream=detail.stream, cgpa=detail.cgpa,
                                          entrance_exam_score=detail.entrance_exam_score)

            db.add(new_details)
            db.commit()
            db.refresh(new_details)
    return templates.TemplateResponse("two.html", {"request": request, "details": details})
