#Define the SQLModel Model:

from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional

class SQLModelUser(SQLModel, table=True):
    userID: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    email: str
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    dateofbirth: Optional[date] = None
    goalID: Optional[int] = None
    routineID: Optional[int] = None
    nutritionID: Optional[int] = None
    professionalID: Optional[int] = None

#Create the Database Engine and Tables:

sqlite_file_name = "users.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)  # echo=True shows SQL statements

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


#Implement the SQLModel Repository Class:

class SQLModelUserRepository(UserRepository):
    def __init__(self, engine):
        self.engine = engine
        create_db_and_tables() #Create tables if they do not exist.

    def create(self, user: UserCreate) -> User:
        with Session(self.engine) as session:
            db_user = SQLModelUser(**user.dict())
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return User(**db_user.__dict__)

    def get(self, user_id: int) -> Optional[User]:
        with Session(self.engine) as session:
            db_user = session.get(SQLModelUser, user_id)
            if db_user:
                return User(**db_user.__dict__)
            return None

    def get_all(self) -> List[User]:
        with Session(self.engine) as session:
            users = session.exec(select(SQLModelUser)).all()
            return [User(**user.__dict__) for user in users]

    def update(self, user_id: int, user: UserCreate) -> User:
        with Session(self.engine) as session:
            db_user = session.get(SQLModelUser, user_id)
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            for key, value in user.dict().items():
                setattr(db_user, key, value)
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return User(**db_user.__dict__)

    def delete(self, user_id: int):
        with Session(self.engine) as session:
            db_user = session.get(SQLModelUser, user_id)
            if not db_user:
                raise HTTPException(status_code=404, detail="User not found")
            session.delete(db_user)
            session.commit()

#FastAPI Integration (Example):

@app.post("/users/", response_model=User)
def create_user(user: UserCreate):
    repo = SQLModelUserRepository(engine)
    return repo.create(user)

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    repo = SQLModelUserRepository(engine)
    db_user = repo.get(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Add other routes for get_all, update, and delete...
