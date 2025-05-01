def generate_mermaid_erd(mermaid_code):
    """
    Generates an HTML file containing a Mermaid ERD diagram from the provided Mermaid code.

    Args:
        mermaid_code (str): The Mermaid code defining the ERD.
    """
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ERD Diagram</title>
        <script src="https://cdn.jsdelivr.net/npm/mermaid@10.8.0/dist/mermaid.min.js"></script>
        <script>
            mermaid.initialize({{ startOnLoad: true }});
        </script>
    </head>
    <body>
        <div class="mermaid">
            {mermaid_code}
        </div>
    </body>
    </html>
    """

    with open("erd_diagram.html", "w") as f:
        f.write(html_template)

    print("ERD diagram generated successfully as erd_diagram.html")

if __name__ == "__main__":
    mermaid_input = """
    erDiagram

        User {{
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
        }}

        Professionals {{
            varchar username
            varchar password
            varchar email
            varchar profession
            varchar specialty
            int routineID FK
            int nutritionID FK
            int professionalID PK
        }}

        Goal {{
            int goalID PK
            int userID FK
            varchar goaltype
            float goalvalue
            date startdate
            date enddate
        }}

        Activity {{
            int activityID PK
            date activitydate
            time starttime
            time endtime
            varchar activitytype
        }}

        Routine {{
            int routineID PK
            int activityID FK
        }}

        Food {{
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
        }}

        Meal {{
            int mealID PK
            int nutritionID FK
            date mealdate
            time mealtime
            varchar mealtype
        }}

        Nutrition {{
            int nutritionID PK
            int mealID FK
        }}

        Client {{
            int clientID PK
            int userID FK
        }}

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
    """
    generate_mermaid_erd(mermaid_input)
