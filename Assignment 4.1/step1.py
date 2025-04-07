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

# ... (Data Models as provided) ...

from .definefields import UserCreate, User, GoalCreate, Goal, ActivityCreate, Activity, RoutineCreate, Routine, FoodCreate, Food, MealCreate, Meal, NutritionCreate, Nutrition, ClientCreate, Client, ProfessionalsCreate, Professionals  

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
    username: str
    password: str
    email: str
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
    FoodName: str
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
    username: str
    password: str
    email: str
    profession: str
    specialty: str
    routineID: Optional[int] = Field(default=None, foreign_key="routine.routineID")
    nutritionID: Optional[int] = Field(default=None, foreign_key="nutrition.nutritionID")

class SQLModelRepository(Repository):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        SQLModel.metadata.create_all(self.engine)

    def create_user(self, user: UserCreate) -> User:
        with Session(self.engine) as session:
            db_user = SQLModelUser(**user.dict())
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return User(**db_user.__dict__)

    def get_user(self, user_id: int) -> Optional[User]:
        with Session(self.engine) as session:
            db_user = session.get(SQLModelUser, user_id)
            if db_user:
                return User(**db_user.__dict__)
            return None

    def get_all_users(self) -> List[User]:
        with Session(self.engine) as session:
            users = session.exec(select(SQLModelUser)).all()
            return [User(**user.__dict__) for user in users]

    def create_goal(self, goal: GoalCreate) -> Goal:
        with Session(self.engine) as session:
            db_goal = SQLModelGoal(**goal.dict())
            session.add(db_goal)
            session.commit()
            session.refresh(db_goal)
            return Goal(**db_goal.__dict__)

    def get_goal(self, goal_id: int) -> Optional[Goal]:
        with Session(self.engine) as session:
            db_goal = session.get(SQLModelGoal, goal_id)
            if db_goal:
                return Goal(**db_goal.__dict__)
            return None

    def create_activity(self, activity: ActivityCreate) -> Activity:
        with Session(self.engine) as session:
            db_activity = SQLModelActivity(**activity.dict())
            session.add(db_activity)
            session.commit()
            session.refresh(db_activity)
            return Activity(**db_activity.__dict__)

    def get_activity(self, activity_id: int) -> Optional[Activity]:
        with Session(self.engine) as session:
            db_activity = session.get(SQLModelActivity, activity_id)
            if db_activity:
                return Activity(**db_activity.__dict__)
            return None

    def create_routine(self, routine: RoutineCreate) -> Routine:
        with Session(self.engine) as session:
            db_routine = SQLModelRoutine(**routine.dict())
            session.add(db_routine)
            session.commit()
            session.refresh(db_routine)
            return Routine(**db_routine.__dict__)

    def get_routine(self, routine_id: int) -> Optional[Routine]:
        with Session(self.engine) as session:
            db_routine = session.get(SQLModelRoutine, routine_id)
            if db_routine:
                return Routine(**db_routine.__dict__)
            return None

    def create_food(self, food: FoodCreate) -> Food:
        with Session(self.engine) as session:
            db_food = SQLModelFood(**food.dict())
            session.add(db_food)
            session.commit()
            session.refresh(db_food)
            return Food(**db_food.__dict__)

    def get_food(self, food_id: int) -> Optional[Food]:
        with Session(self.engine) as session:
            db_food = session.get(SQLModelFood, food_id)
            if db_food:
                return Food(**db_food.__dict__)
            return None

    def create_meal(self, meal: MealCreate) -> Meal:
        with Session(self.engine) as session:
            db_meal = SQLModelMeal(**meal.dict())
            session.add(db_meal)
            session.commit()
            session.refresh(db_meal)
            return Meal(**db_meal.__dict__)

    def get_meal(self, meal_id: int) -> Optional[Meal]:
        with Session(self.engine) as session:
            db_meal = session.get(SQLModelMeal, meal_id)
            if db_meal:
                return Meal(**db_meal.__dict__)
            return None

    def create_nutrition(self, nutrition: NutritionCreate) -> Nutrition:
        with Session(self.engine) as session:
            db_nutrition = SQLModelNutrition(**nutrition.dict())
            session.add(db_nutrition)
            session.commit()
            session.refresh(db_nutrition)
            return Nutrition(**db_nutrition.__dict__)

    def get_nutrition(self, nutrition_id: int) -> Optional[Nutrition]:
        with Session(self.engine) as session:
            db_nutrition = session.get(SQLModelNutrition, nutrition_id)
            if db_nutrition:
                return Nutrition(**db_nutrition.__dict__)
            return None

    def create_client(self, client: ClientCreate) -> Client:
        with Session(self.engine) as session:
            db_client = SQLModelClient(**client.dict())
            session.add(db_client)
            session.commit()
            session.refresh(db_client)
            return Client(**db_client.__dict__)

    def get_client(self, client_id: int) -> Optional[Client]:
        with Session(self.engine) as session:
            db_client = session.get(SQLModelClient, client_id)
            if db_client:
                return Client(**db_client.__dict__)
            return None

    def create_professional(self, professional: ProfessionalsCreate) -> Professionals:
        with Session(self.engine) as session:
            db_professional = SQLModelProfessionals(**professional.dict())
            session.add(db_professional)
            session.commit()
            session.refresh(db_professional)
            return Professionals(**db_professional.__dict__)

    def get_professional(self, professional_id: int) -> Optional[Professionals]:
        with Session(self.engine) as session:
            db_professional = session.get(SQLModelProfessionals, professional_id)
            if db_professional:
                return Professionals(**db_professional.__dict__)
            return None

# --- FastAPI Dependency Injection ---
def get_repository() -> Repository:
    db_url = "sqlite:///./test.db"  # Example DB URL
    return SQLModelRepository(db_url)

# --- FastAPI API Routes ---

# ... (API Routes as provided) ...