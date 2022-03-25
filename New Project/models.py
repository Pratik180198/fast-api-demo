from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class BlogTable(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True,)
    blog = Column(String(30))
    body = Column(String(100))
    user_id = Column(Integer, ForeignKey('users.id'))

    creator = relationship("UserTable", back_populates="blogs")


class UserTable(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True)
    email = Column(String(30), unique=True)
    password = Column(String(100))

    blogs = relationship("BlogTable", back_populates="creator")
