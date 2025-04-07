# Django REST Framework Implementation using Django ORM directly

from datetime import date, time
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response
from django.db import models
from rest_framework.decorators import action

# Django Models
class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    height = models.FloatField()
    weight = models.FloatField()
    dateofbirth = models.DateField()
    goalID = models.ForeignKey('Goal', on_delete=models.SET_NULL, null=True, blank=True)
    routineID = models.ForeignKey('Routine', on_delete=models.SET_NULL, null=True, blank=True)
    nutritionID = models.ForeignKey('Nutrition', on_delete=models.SET_NULL, null=True, blank=True)
    professionalID = models.ForeignKey('Professionals', on_delete=models.SET_NULL, null=True, blank=True)

class Goal(models.Model):
    userID = models.IntegerField()
    goaltype = models.CharField(max_length=255)
    goalvalue = models.FloatField()
    startdate = models.DateField()
    enddate = models.DateField()

class Activity(models.Model):
    activitydate = models.DateField()
    starttime = models.TimeField()
    endtime = models.TimeField()
    activitytype = models.CharField(max_length=255)

class Routine(models.Model):
    activityID = models.IntegerField()

class Food(models.Model):
    FoodName = models.CharField(max_length=255)
    FoodBrand = models.CharField(max_length=255, null=True, blank=True)
    servingsize = models.FloatField()
    servingunit = models.CharField(max_length=255)
    calories = models.FloatField()
    protein = models.FloatField()
    carbohydrates = models.FloatField()
    fat = models.FloatField()
    sodium = models.FloatField()

class Meal(models.Model):
    nutritionID = models.IntegerField()
    mealdate = models.DateField()
    mealtime = models.TimeField()
    mealtype = models.CharField(max_length=255)

class Nutrition(models.Model):
    mealID = models.IntegerField()

class Client(models.Model):
    userID = models.IntegerField()

class Professionals(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    profession = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    routineID = models.ForeignKey('Routine', on_delete=models.SET_NULL, null=True, blank=True)
    nutritionID = models.ForeignKey('Nutrition', on_delete=models.SET_NULL, null=True, blank=True)

# Serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'

class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = '__all__'

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = '__all__'

class NutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nutrition
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class ProfessionalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professionals
        fields = '__all__'

# Viewsets
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class RoutineViewSet(viewsets.ModelViewSet):
    queryset = Routine.objects.all()
    serializer_class = RoutineSerializer

class FoodViewSet(viewsets.ModelViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class NutritionViewSet(viewsets.ModelViewSet):
    queryset = Nutrition.objects.all()
    serializer_class = NutritionSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ProfessionalsViewSet(viewsets.ModelViewSet):
    queryset = Professionals.objects.all()
    serializer_class = ProfessionalsSerializer

# urls.py (example)
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'goals', GoalViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'routines', RoutineViewSet)
router.register(r'foods', FoodViewSet)
router.register(r'meals', MealViewSet)
router.register(r'nutritions', NutritionViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'professionals', ProfessionalsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]