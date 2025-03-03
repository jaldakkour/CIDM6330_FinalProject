#Create an API in Python using FastAPI (we'll switch to Django later)
mkdir health_api
cd health_api
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install fastapi uvicorn pydantic python-dotenv sqlalchemy psycopg2-binary
git init


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import Column, Integer, String, Date, Float, Time, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    userID = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    gender = Column(String)
    height = Column(Float)
    weight = Column(Float)
    dateofbirth = Column(Date)
    goalID = Column(Integer, ForeignKey("goals.goalID"))
    routineID = Column(Integer, ForeignKey("routines.routineID"))
    nutritionID = Column(Integer, ForeignKey("nutritions.nutritionID"))
    professionalID = Column(Integer, ForeignKey("professionals.professionalID"))
    goals = relationship("Goal", back_populates="users")
    routines = relationship("Routine", back_populates="users")
    nutritions = relationship("Nutrition", back_populates="users")
    professionals = relationship("Professionals", back_populates="users")
    clients = relationship("Client", back_populates="users")

class Professionals(Base):
    __tablename__ = "professionals"
    professionalID = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
    email = Column(String)
    profession = Column(String)
    specialty = Column(String)
    routineID = Column(Integer, ForeignKey("routines.routineID"))
    nutritionID = Column(Integer, ForeignKey("nutritions.nutritionID"))
    routines = relationship("Routine", back_populates="professionals")
    nutritions = relationship("Nutrition", back_populates="professionals")
    users = relationship("User", back_populates="professionals")
    clients = relationship("Client", back_populates="professionals")

class Goal(Base):
    __tablename__ = "goals"
    goalID = Column(Integer, primary_key=True, index=True)
    userID = Column(Integer, ForeignKey("users.userID"))
    goaltype = Column(String)
    goalvalue = Column(Float)
    startdate = Column(Date)
    enddate = Column(Date)
    users = relationship("User", back_populates="goals")

# ... (Implement other models: Activity, Routine, Food, Meal, Nutrition, Client)

from pydantic import BaseModel
from datetime import date, time

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str
    gender: str
    height: float
    weight: float
    dateofbirth: date
    goalID: int
    routineID: int
    nutritionID: int
    professionalID: int

class User(UserBase):
    userID: int
    class Config:
        orm_mode = True

# ... (Implement schemas for other models)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import schemas, models
from ..database import get_db

router = APIRouter()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# ... (Implement other CRUD operations)

from fastapi import FastAPI
from . import models, database
from .routers import users, professionals, goals, activities, routines, foods, meals, nutritions, clients

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(professionals.router)
app.include_router(goals.router)
app.include_router(activities.router)
app.include_router(routines.router)
app.include_router(foods.router)
app.include_router(meals.router)
app.include_router(nutritions.router)
app.include_router(clients.router)

git add .
git commit -m "Initial commit"
git remote add origin your_github_repo_url
git branch -M main
git push -u origin main
