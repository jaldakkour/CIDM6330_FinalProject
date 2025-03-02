erDiagram
```mermaid
<
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
    User ||--o{ Routine : has
    User ||--o{ Nutrition : has
    User ||--o{ Professionals : assigned to
    Professionals ||--o{ Routine : creates
    Professionals ||--o{ Nutrition : creates
    Professionals ||--o{ User : manages
    Goal }o--|| User : belongs to
    Routine }o--|| User : part of
    Nutrition }o--|| User : part of
    Routine }o--|| Activity : includes
    Meal }o--|| Nutrition : contains
    Nutrition }o--|| Meal : contains
    User ||--o{ Client: is
    Client }o--|| User: is
               
    >
