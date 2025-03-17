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
        
# --- In-Memory Repository ---

class InMemoryRepository(Repository):
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.goals: Dict[int, Goal] = {}
        self.activities: Dict[int, Activity] = {}
        self.routines: Dict[int, Routine] = {}
        self.foods: Dict[int, Food] = {}
        self.meals: Dict[int, Meal] = {}
        self.nutritions: Dict[int, Nutrition] = {}
        self.clients: Dict[int, Client] = {}
        self.professionals: Dict[int, Professionals] = {}

        self.next_user_id = 1
        self.next_goal_id = 1
        self.next_activity_id = 1
        self.next_routine_id = 1
        self.next_food_id = 1
        self.next_meal_id = 1
        self.next_nutrition_id = 1
        self.next_client_id = 1
        self.next_professional_id = 1

    def create_user(self, user: UserCreate) -> User:
        user_id = self.next_user_id
        self.next_user_id += 1
        new_user = User(userID=user_id, **user.dict())
        self.users[user_id] = new_user
        return new_user

    def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)

    def get_all_users(self) -> List[User]:
        return list(self.users.values())

    def create_goal(self, goal: GoalCreate) -> Goal:
        goal_id = self.next_goal_id
        self.next_goal_id += 1
        new_goal = Goal(goalID=goal_id, **goal.dict())
        self.goals[goal_id] = new_goal
        return new_goal

    def get_goal(self, goal_id: int) -> Optional[Goal]:
        return self.goals.get(goal_id)

    def create_activity(self, activity: ActivityCreate) -> Activity:
        activity_id = self.next_activity_id
        self.next_activity_id += 1
        new_activity = Activity(activityID=activity_id, **activity.dict())
        self.activities[activity_id] = new_activity
        return new_activity

    def get_activity(self, activity_id: int) -> Optional[Activity]:
        return self.activities.get(activity_id)

    def create_routine(self, routine: RoutineCreate) -> Routine:
        routine_id = self.next_routine_id
        self.next_routine_id += 1
        new_routine = Routine(routineID=routine_id, **routine.dict())
        self.routines[routine_id] = new_routine
        return new_routine

    def get_routine(self, routine_id: int) -> Optional[Routine]:
        return self.routines.get(routine_id)

    def create_food(self, food: FoodCreate) -> Food:
        food_id = self.next_food_id
        self.next_food_id += 1
        new_food = Food(foodID=food_id, **food.dict())
        self.foods[food_id] = new_food
        return new_food

    def get_food(self, food_id: int) -> Optional[Food]:
        return self.foods.get(food_id)

    def create_meal(self, meal: MealCreate) -> Meal:
        meal_id = self.next_meal_id
        self.next_meal_id += 1
        new_meal = Meal(mealID=meal_id, **meal.dict())
        self.meals[meal_id] = new_meal
        return new_meal

    def get_meal(self, meal_id: int) -> Optional[Meal]:
        return self.meals.get(meal_id)

    def create_nutrition(self, nutrition: NutritionCreate) -> Nutrition:
        nutrition_id = self.next_nutrition_id
        self.next_nutrition_id += 1
        new_nutrition = Nutrition(nutritionID=nutrition_id, **nutrition.dict())
        self.nutritions[nutrition_id] = new_nutrition
        return new_nutrition

    def get_nutrition(self, nutrition_id: int) -> Optional[Nutrition]:
        return self.nutritions.get(nutrition_id)

    def create_client(self, client: ClientCreate) -> Client:
        client_id = self.next_client_id
        self.next_client_id += 1
        new_client = Client(clientID=client_id, **client.dict())
        self.clients[client_id] = new_client
        return new_client

    def get_client(self, client_id: int) -> Optional[Client]:
        return self.clients.get(client_id)

    def create_professional(self, professional: ProfessionalsCreate) -> Professionals:
        professional_id = self.next_professional_id
        self.next_professional_id += 1
        new_professional = Professionals(professionalID=professional_id, **professional.dict())
        self.professionals[professional_id] = new_professional
        return new_professional

    def get_professional(self, professional_id: int) -> Optional[Professionals]:
        return self.professionals.get(professional_id)


# --- FastAPI Dependency Injection ---
def get_repository() -> Repository:
    return InMemoryRepository()

# --- FastAPI API Routes ---

# User routes
@app.post("/users/", response_model=User)
def create_user(user: UserCreate, repo: Repository = Depends(get_repository)):
    return repo.create_user(user)

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, repo: Repository = Depends(get_repository)):
    db_user = repo.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/", response_model=List[User])
def read_all_users(repo: Repository = Depends(get_repository)):
    return repo.get_all_users()

# Goal routes
@app.post("/goals/", response_model=Goal)
def create_goal(goal: GoalCreate, repo: Repository = Depends(get_repository)):
    return repo.create_goal(goal)

@app.get("/goals/{goal_id}", response_model=Goal)
def read_goal(goal_id: int, repo: Repository = Depends(get_repository)):
    db_goal = repo.get_goal(goal_id)
    if db_goal is None:
        raise HTTPException(status_code=404, detail="Goal not found")
    return db_goal

# Activity routes
@app.post("/activities/", response_model=Activity)
def create_activity(activity: ActivityCreate, repo: Repository = Depends(get_repository)):
    return repo.create_activity(activity)

@app.get("/activities/{activity_id}", response_model=Activity)
def read_activity(activity_id: int, repo: Repository = Depends(get_repository)):
    db_activity = repo.get_activity(activity_id)
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return db_activity

# Routine routes
@app.post("/routines/", response_model=Routine)
def create_routine(routine: RoutineCreate, repo: Repository = Depends(get_repository)):
    return repo.create_routine(routine)

@app.get("/routines/{routine_id}", response_model=Routine)
def read_routine(routine_id: int, repo: Repository = Depends(get_repository)):
    db_routine = repo.get_routine(routine_id)
    if db_routine is None:
        raise HTTPException(status_code=404, detail="Routine not found")
    return db_routine

# Food routes
@app.post("/foods/", response_model=Food)
def create_food(food: FoodCreate, repo: Repository = Depends(get_repository)):
    return repo.create_food(food)

@app.get("/foods/{food_id}", response_model=Food)
def read_food(food_id: int, repo: Repository = Depends(get_repository)):
    db_food = repo.get_food(food_id)
    if db_food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return db_food

# Meal routes
@app.post("/meals/", response_model=Meal)
def create_meal(meal: MealCreate, repo: Repository = Depends(get_repository)):
    return repo.create_meal(meal)

@app.get("/meals/{meal_id}", response_model=Meal)
def read_meal(meal_id: int, repo: Repository = Depends(get_repository)):
    db_meal = repo.get_meal(meal_id)
    if db_meal is None:
        raise HTTPException(status_code=404, detail="Meal not found")
    return db_meal

# Nutrition routes
@app.post("/nutritions/", response_model=Nutrition)
def create_nutrition(nutrition: NutritionCreate, repo: Repository = Depends(get_repository)):
    return repo.create_nutrition(nutrition)

@app.get("/nutritions/{nutrition_id}", response_model=Nutrition)
def read_nutrition(nutrition_id: int, repo: Repository = Depends(get_repository)):
    db_nutrition = repo.get_nutrition(nutrition_id)
    if db_nutrition is None:
        raise HTTPException(status_code=404, detail="Nutrition not found")
    return db_nutrition

# Client routes
@app.post("/clients/", response_model=Client)
def create_client(client: ClientCreate, repo: Repository = Depends(get_repository)):
    return repo.create_client(client)

@app.get("/clients/{client_id}", response_model=Client)
def read_client(client_id: int, repo: Repository = Depends(get_repository)):
    db_client = repo.get_client(client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

# Professional routes
@app.post("/professionals/", response_model=Professionals)
def create_professional(professional: ProfessionalsCreate, repo: Repository = Depends(get_repository)):
    return repo.create_professional(professional)

@app.get("/professionals/{professional_id}", response_model=Professionals)
def read_professional(professional_id: int, repo: Repository = Depends(get_repository)):
    db_professional = repo.get_professional(professional_id)
    if db_professional is None:
        raise HTTPException(status_code=404, detail="Professional not found")
    return db_professional
