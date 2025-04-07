from typing import List, Optional, Dict
from datetime import date, time
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from abc import ABC, abstractmethod
import csv
import json
import sqlite3
from sqlmodel import SQLModel, Field, create_engine, Session, select

app = FastAPI()

### --- Data Models ---

class UserBase(BaseModel):
    username: str
    password: str
    email: str
    gender: str
    height: float
    weight: float
    dateofbirth: date
    goalID: Optional[int] = None
    routineID: Optional[int] = None
    nutritionID: Optional[int] = None
    professionalID: Optional[int] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    userID: int

class GoalBase(BaseModel):
    userID: int
    goaltype: str
    goalvalue: float
    startdate: date
    enddate: date

class GoalCreate(GoalBase):
    pass

class Goal(GoalBase):
    goalID: int

class ActivityBase(BaseModel):
    activitydate: date
    starttime: time
    endtime: time
    activitytype: str

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    activityID: int

class RoutineBase(BaseModel):
    activityID: int

class RoutineCreate(RoutineBase):
    pass

class Routine(RoutineBase):
    routineID: int

class FoodBase(BaseModel):
    FoodName: str
    FoodBrand: Optional[str] = None
    servingsize: float
    servingunit: str
    calories: float
    protein: float
    carbohydrates: float
    fat: float
    sodium: float

class FoodCreate(FoodBase):
    pass

class Food(FoodBase):
    foodID: int

class MealBase(BaseModel):
    nutritionID: int
    mealdate: date
    mealtime: time
    mealtype: str

class MealCreate(MealBase):
    pass

class Meal(MealBase):
    mealID: int

class NutritionBase(BaseModel):
    mealID: int

class NutritionCreate(NutritionBase):
    pass

class Nutrition(NutritionBase):
    nutritionID: int

class ClientBase(BaseModel):
    userID: int

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    clientID: int

class ProfessionalsBase(BaseModel):
    username: str
    password: str
    email: str
    profession: str
    specialty: str
    routineID: Optional[int] = None
    nutritionID: Optional[int] = None

class ProfessionalsCreate(ProfessionalsBase):
    pass

class Professionals(ProfessionalsBase):
    professionalID: int

### --- Repository Interfaces ---

class Repository(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate) -> User:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        pass

    @abstractmethod
    def create_goal(self, goal: GoalCreate) -> Goal:
        pass

    @abstractmethod
    def get_goal(self, goal_id: int) -> Optional[Goal]:
        pass

    @abstractmethod
    def create_activity(self, activity: ActivityCreate) -> Activity:
        pass

    @abstractmethod
    def get_activity(self, activity_id: int) -> Optional[Activity]:
        pass

    @abstractmethod
    def create_routine(self, routine: RoutineCreate) -> Routine:
        pass

    @abstractmethod
    def get_routine(self, routine_id: int) -> Optional[Routine]:
        pass

    @abstractmethod
    def create_food(self, food: FoodCreate) -> Food:
        pass

    @abstractmethod
    def get_food(self, food_id: int) -> Optional[Food]:
        pass

    @abstractmethod
    def create_meal(self, meal: MealCreate) -> Meal:
        pass

    @abstractmethod
    def get_meal(self, meal_id: int) -> Optional[Meal]:
        pass

    @abstractmethod
    def create_nutrition(self, nutrition: NutritionCreate) -> Nutrition:
        pass

    @abstractmethod
    def get_nutrition(self, nutrition_id: int) -> Optional[Nutrition]:
        pass

    @abstractmethod
    def create_client(self, client: ClientCreate) -> Client:
        pass

    @abstractmethod
    def get_client(self, client_id: int) -> Optional[Client]:
        pass

    @abstractmethod
    def create_professional(self, professional: ProfessionalsCreate) -> Professionals:
        pass

    @abstractmethod
    def get_professional(self, professional_id: int) -> Optional[Professionals]:
        pass

### --- SQLModel Repository ---

class SQLModelUser(SQLModel, table=True):
    userID: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str
    email: str = Field(index=True)
    gender: str
    height: float
    weight: float
    dateofbirth: date
    goalID: Optional[int] = Field(default=None, foreign_key="goal.goalID")
    routineID: Optional[int] = Field(default=None, foreign_key="routine.routineID")
    nutritionID: Optional[int] = Field(default=None, foreign_key="nutrition.nutritionID")
    professionalID: Optional[int] = Field(default=None, foreign_key="professionals.professionalID")

class SQLModelGoal(SQLModel, table=True):
    goalID: Optional[int] = Field(default=None, primary_key=True)
    userID: int
    goaltype: str
    goalvalue: float
    startdate: date
    enddate: date

class SQLModelActivity(SQLModel, table=True):
    activityID: Optional[int] = Field(default=None, primary_key=True)
    activitydate: date
    starttime: time
    endtime: time
    activitytype: str

class SQLModelRoutine(SQLModel, table=True):
    routineID: Optional[int] = Field(default=None, primary_key=True)
    activityID: int

class SQLModelFood(SQLModel, table=True):
    foodID: Optional[int] = Field(default=None, primary_key=True)
    FoodName: str = Field(index=True)
    FoodBrand: Optional[str]
    servingsize: float
    servingunit: str
    calories: float
    protein: float
    carbohydrates: float
    fat: float
    sodium: float

class SQLModelMeal(SQLModel, table=True):
    mealID: Optional[int] = Field(default=None, primary_key=True)
    nutritionID: int
    mealdate: date
    mealtime: time
    mealtype: str

class SQLModelNutrition(SQLModel, table=True):
    nutritionID: Optional[int] = Field(default=None, primary_key=True)
    mealID: int

class SQLModelClient(SQLModel, table=True):
    clientID: Optional[int] = Field(default=None, primary_key=True)
    userID: int

class SQLModelProfessionals(SQLModel, table=True):
    professionalID: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    password: str
    email: str = Field(index=True)
    profession: str
    specialty: str
    routineID: Optional[int] = Field(default=None, foreign_key="routine.routineID")
    nutritionID: Optional[int] = Field(default=None, foreign_key="nutrition.nutritionID")

class SQLModelRepository(Repository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self)


  
