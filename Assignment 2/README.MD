#1.Create an Entity Relationship Diagram
```mermaid
erDiagram
   
    User {
        varchar username
        varchar password
        varchar email
        varchar gender
        float height
        float weight
        date dateofbirth
        int goalID FK
        int routineID FK
        int nutritionID FK
        int professionalID FK
        int userID PK
    }

    Professionals {
        varchar username
        varchar password
        varchar email
        varchar profession
        varchar specialty
        int routineID FK
        int nutritionID FK
        int professionalID PK
    }

    Goal {
        int goalID PK
        int userID FK
        varchar goaltype
        float goalvalue
        date startdate
        date enddate
    }

    Activity {
        int activityID PK
        date activitydate
        time starttime
        time endtime
        varchar activitytype
    }

    Routine {
        int routineID PK
        int activityID FK
    }

    Food {
        int foodID PK
        varchar FoodName
        varchar FoodBrand
        float servingsize
        varchar servingunit
        float calories
        float protein
        float carbohydrates
        float fat
        float sodium
    }

    Meal {
        int mealID PK
        int nutritionID FK
        date mealdate
        time mealtime
        varchar mealtype
    }

    Nutrition {
        int nutritionID PK
        int mealID FK
    }

    Client {
        int clientID PK
        int userID FK
    }

    User ||--o{ Goal : has
    User ||--o{ Routine : creates
    User ||--o{ Food : enters
    User ||--o{ Professionals : communicates_with
    Professionals ||--o{ Routine : creates
    Professionals ||--o{ Meal : creates
    Professionals ||--o{ User : works_with
    Goal }o--|| User : belongs 
    Routine }o--|| User : used_by
    Nutrition }o--|| User : part_of
    Routine }o--|| Activity : includes
    Food }o--|| Meal: eaten_during 
    Meal }o--|| Nutrition: contains
    Client }o--|| Professionals: has
    Client }o--|| User: is
``` 

#2.Create an API in Python using FastAPI (we'll switch to Django later)


#3.Create Pydantic models that mirror your ERD and assist to validate Create, Read, Update, Delete (CRUD) apps for your ERD

#4.Develop an initial set of CRUD transactions that would begin to develop and use the entities from your domain. We are not implementing any meaningful logic right now, just simply performaing basic state (CRUD) operations


