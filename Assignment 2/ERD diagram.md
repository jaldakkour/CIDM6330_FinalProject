def generate_mermaid_erd(mermaid_code, filename="erd_diagram.html"):
    """
    Generates an HTML file containing a Mermaid ERD diagram from the provided Mermaid code.
    The HTML file is saved with a default name of "erd_diagram.html" or a user-specified filename.

    Args:
        mermaid_code (str): The Mermaid code defining the ERD.
        filename (str, optional): The name of the HTML file to save. Defaults to "erd_diagram.html".
    """
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ERD Diagram</title>
        <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
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

    with open(filename, "w") as f:
        f.write(html_template)

    print(f"ERD diagram generated successfully as {filename}")

if __name__ == "__main__":
    mermaid_input = """
    erDiagram
        %% Entities
        User {
            int userID PK
            varchar username
            varchar password
            varchar email
            varchar gender
            float height
            float weight
            date dateOfBirth
            int goalID FK
            int routineID FK
            int nutritionID FK
            int professionalID FK
        }
        Professionals {
            int professionalID PK
            varchar username
            varchar password
            varchar email
            varchar profession
            varchar specialty
            int routineID FK
            int nutritionID FK
        }
        Goal {
            int goalID PK
            int userID FK
            varchar goalType
            float goalValue
            date startDate
            date endDate
        }
        Activity {
            int activityID PK
            date activityDate
            time startTime
            time endTime
            varchar activityType
        }
        Routine {
            int routineID PK
            int activityID FK
        }
        Food {
            int foodID PK
            varchar foodName
            varchar foodBrand
            float servingSize
            varchar servingUnit
            float calories
            float protein
            float carbohydrates
            float fat
            float sodium
        }
        Meal {
            int mealID PK
            int nutritionID FK
            date mealDate
            time mealTime
            varchar mealType
        }
        Nutrition {
            int nutritionID PK
            int mealID FK
        }
        Client {
            int clientID PK
            int userID FK
        }

        %% Relationships
        User ||--o{ Goal : "has"
        User ||--o{ Routine : "creates"
        User ||--o{ Food : "enters"
        User ||--o{ Professionals : "communicates_with"
        Professionals ||--o{ Routine : "creates"
        Professionals ||--o{ Meal : "creates"
        Professionals ||--o{ User : "works_with"
        Goal }o--|| User : "belongs_to"
        Routine }o--|| User : "used_by"
        Nutrition }o--|| User : "part_of"
        Routine ||--o{ Activity : "includes"
        Food ||--o{ Meal : "eaten_during"
        Meal ||--o{ Nutrition : "contains"
        Client ||--o{ Professionals : "has"
        Client ||--o{ User : "is"

        %% Addressed issues:
        %% 1. Consistent Naming:  Changed "dateofbirth" to "dateOfBirth", "FoodName" to "foodName" for consistency.
        %% 2. Explicit Cardinality: Added labels like "has", "creates", etc., to the relationships for clarity.
        %% 3. Relationship Direction:  Made sure the relationship directions are logical (e.g., User creates Routine, not the other way around).
        %% 4. Corrected Relationship Labels: Changed "belongs" to "belongs_to" for better readability.
        %% 5. Added PK and FK to the attributes.
    """
    generate_mermaid_erd(mermaid_input, filename="erd_diagram.html") #You can change the filename here
    # generate_mermaid_erd(mermaid_input, filename="my_erd.html")  # Example of changing the filename
