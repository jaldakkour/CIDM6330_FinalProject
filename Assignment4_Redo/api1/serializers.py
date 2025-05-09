from rest_framework import serializers
from .models import User, Professional, Goal, Activity, Routine, Food, Meal, Nutrition, Client  # Import your models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Or specify fields

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'gender', 'height', 'weight', 'dateofbirth', 'goalID', 'routineID', 'nutritionID', 'professionalID']


# Similar serializers for Professional, Goal, Activity, Routine, Food, Meal, Nutrition, Client
class ProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = '__all__'

class ProfessionalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professional
        fields = ['username', 'password', 'email', 'profession', 'specialty', 'routineID', 'nutritionID']

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class GoalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['userID', 'goaltype', 'goalvalue', 'startdate', 'enddate']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class ActivityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['activitydate', 'starttime', 'endtime', 'activitytype']

class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = '__all__'

class RoutineCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = ['activityID']

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class FoodCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['FoodName', 'FoodBrand', 'servingsize', 'servingunit', 'calories', 'protein', 'carbohydrates', 'fat', 'sodium']


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

class MealCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ['nutritionID', 'mealdate', 'mealtime', 'mealtype']

class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = '__all__'

class NutritionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = ['mealID']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ClientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['userID']

