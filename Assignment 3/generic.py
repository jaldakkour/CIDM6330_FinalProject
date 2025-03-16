from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field, InitVar
import csv



# typehints review

# For most types, just use the name of the type in the annotation
# Note that mypy can usually infer the type of a variable from its value,
# so technically these annotations are redundant
x: int = 1
x: float = 1.0
x: bool = True
x: str = "test"
x: bytes = b"test"

# For collections on Python 3.9+, the type of the collection item is in brackets
x: list[int] = [1]
x: set[int] = {6, 7}

# For mappings, we need the types of both keys and values
x: dict[str, float] = {"field": 2.0}  # Python 3.9+

# For tuples of fixed size, we specify the types of all the elements
x: tuple[int, str, float] = (3, "yes", 7.5)  # Python 3.9+

# For tuples of variable size, we use one type and ellipsis
x: tuple[int, ...] = (1, 2, 3)  # Python 3.9+

# On Python 3.10+, use the | operator when something could be one of a few types
x: list[int | str] = [3, 5, "test", "fun"]  # Python 3.10+

# Data Models (Pydantic)

@dataclass
class UserBase(BaseModel):
    username: str
    password: str
    email: str
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    dateofbirth: Optional[date] = None

class UserCreate(UserBase):
    goalID: Optional[int] = None
    routineID: Optional[int] = None
    nutritionID: Optional[int] = None
    professionalID: Optional[int] = None

class User(UserBase):
    userID: int
    goalID: Optional[int] = None
    routineID: Optional[int] = None
    nutritionID: Optional[int] = None
    professionalID: Optional[int] = None

class ProfessionalBase(BaseModel):
    username: str
    password: str
    email: str
    profession: Optional[str] = None
    specialty: Optional[str] = None

class ProfessionalCreate(ProfessionalBase):
    routineID: Optional[int] = None
    nutritionID: Optional[int] = None

class Professional(ProfessionalBase):
    professionalID: int
    routineID: Optional[int] = None
    nutritionID: Optional[int] = None

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



class MyCSVRepo(BaseProductRepository):
    """
    Note: CSV files don’t maintain data types. All field values are considered str and empty values are considered None.
    """

    def __init__(self, filename: str, id_field: str, fieldnames: list):

        self.repo = list[UserBase] # this is a typehint for a list of User objects
        self.filename = filename
        self.fieldnames = fieldnames

        with open(filename, mode="r", newline="") as file:
            csv_reader = csv.DictReader(file)
            # list comprehension: https://www.w3schools.com/python/python_lists_comprehension.asp
            self.repo = [UserBase(**row) for row in csv_reader]

    def do_create(self, userbase: UserBase):
        self.repo.append(UserBase)
        self.do_save_file()

    def read_all(self):
        return self.repo

    def do_read(self, id):
        return self.repo[str(id)]

    def do_update(self, id, userbase: UserBase):
        self.repo[str(id)] = userbase
        self.do_save_file()

    def do_delete(self, id):
        for userbase in self.repo:
            if int(userbase.id) == int(id):
                self.repo.remove(userbase)
                break

        self.do_save_file()

    def do_save_file(self):
        with open(self.filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            for userbase in self.repo:
                writer.writerow(asdict(userbase))


class MyMemoryRepo(BaseProductRepository):

    def __init__(self, id_field: str):

        self.repo = list[UserBase]

    def do_create(self, userbase: UserBase):
        self.repo.append(userbase)

    def read_all(self):
        return self.repo

    def do_read(self, id):
        return self.repo[id]

    def do_update(self, id, userbase: UserBase):
        self.repo[id] = userbase

    def do_delete(self, id):
        for useerbase in self.repo:
            if int(userbase.id) == int(id):
                self.repo.remove(userbase)
                break
        


# Defining main function
def main():
    print("generic repository example")
    csv_repo = MyCSVRepo("users.csv", "id", ["userid", "firstname", "lastname", "username", "password", "email", "gender", "height", "weight", "dateofbirth"])

     csv_repo.do_create(UserBase(1, "apple", 1.99))
     csv_repo.do_create(UserBase(2, "banana", 0.99))
     csv_repo.do_create(UserBase(3, "cherry", 2.99))

     csv_repo.do_create(UserBase(4, "pear", 1.59))
     csv_repo.do_create(UserBase(5, "raspberry", 1.09))
     csv_repo.do_create(UserBase(6, "lemon", 0.59))
     csv_repo.do_create(UserBase(7, "pineapple", 5.99))

    csv_repo.do_delete(3)

    print(csv_repo.read_all())


# Using the special variable
# __name__
if __name__ == "__main__":
    main()
