from database import Base
from sqlalchemy import Column, Integer, String, Float


class StudentTable(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(30))
    email_id = Column(String(50), unique=True)
    graduation_completed = Column(String(30))
    stream = Column(String(30))
    cgpa = Column(Float(10))
    entrance_exam_score = Column(Integer)


class Stages(Base):
    __tablename__ = 'stages'
    id = Column(Integer)
    full_name = Column(String(30))
    email_id = Column(String(50), primary_key=True, index=True)
    graduation_completed = Column(String(30))
    stream = Column(String(30))
    cgpa = Column(Float(10))
    entrance_exam_score = Column(Integer)


class StageTwo(Base):
    __tablename__ = 'stagetwo'
    id = Column(Integer)
    full_name = Column(String(30))
    email_id = Column(String(50), primary_key=True, index=True)
    graduation_completed = Column(String(30))
    stream = Column(String(30))
    cgpa = Column(Float(10))
    entrance_exam_score = Column(Integer)

