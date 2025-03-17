#Complete the SQLModel Repository:
from typing import List, Optional
from sqlmodel import SQLModel, Session, create_engine, select
from trial import (Nutrition, Activity, ActivityCreate, Client, ClientCreate, Food, FoodCreate, Goal, GoalCreate, Meal, MealCreate, Nutrition, NutritionCreate, Professionals, ProfessionalsCreate, Repository, Routine, RoutineCreate, SQLModelActivity, SQLModelClient, SQLModelFood, SQLModelGoal, SQLModelMeal, SQLModelNutrition, SQLModelProfessionals, SQLModelRoutine, SQLModelUser, User, UserCreate
)

#Database URL (insert later)
DATABASE_URL = "sqlite:///./test.db"  

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
