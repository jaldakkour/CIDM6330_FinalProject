from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Professional,
    Goal,
    Activity,
    Routine,
    Food,
    Meal,
    Nutrition,
    Client,
    UserProfile,
    MealFood,
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')  # Include necessary fields

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the UserProfile model."""
    user = UserSerializer()  # Nest the UserSerializer
    class Meta:
        model = UserProfile
        fields = '__all__'
        #read_only_fields = ('user',)  # Prevent user field from being modified


class ProfessionalSerializer(serializers.ModelSerializer):
    """Serializer for the Professional model."""
    class Meta:
        model = Professional
        fields = '__all__'


class GoalSerializer(serializers.ModelSerializer):
    """Serializer for the Goal model."""
    class Meta:
        model = Goal
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for the Activity model."""
    class Meta:
        model = Activity
        fields = '__all__'



class RoutineSerializer(serializers.ModelSerializer):
    """Serializer for the Routine model."""
    activities = ActivitySerializer(many=True)
    class Meta:
        model = Routine
        fields = '__all__'



class FoodSerializer(serializers.ModelSerializer):
    """Serializer for the Food model."""
    class Meta:
        model = Food
        fields = '__all__'



class MealFoodSerializer(serializers.ModelSerializer):
    """Serializer for the MealFood through model"""
    food = FoodSerializer()
    class Meta:
        model = MealFood
        fields = '__all__'

class MealSerializer(serializers.ModelSerializer):
    """Serializer for the Meal model."""
    # foods = FoodSerializer(many=True)  # Use MealFoodSerializer
    meals = MealFoodSerializer(many=True, read_only=True)
    class Meta:
        model = Meal
        fields = '__all__'



class NutritionSerializer(serializers.ModelSerializer):
    """Serializer for the Nutrition model."""
    meals = MealSerializer(many=True)
    class Meta:
        model = Nutrition
        fields = '__all__'



class ClientSerializer(serializers.ModelSerializer):
    """Serializer for the Client model."""
    user = UserProfileSerializer()
    class Meta:
        model = Client
        fields = '__all__'
