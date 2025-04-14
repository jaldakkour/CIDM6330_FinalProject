from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date, time
from unittest.mock import patch

from .models import (
    User, Goal, Activity, Routine, Food, Meal, Nutrition, Client, Professionals
)
from .serializers import (
    UserSerializer, GoalSerializer, ActivitySerializer, RoutineSerializer,
    FoodSerializer, MealSerializer, NutritionSerializer, ClientSerializer,
    ProfessionalsSerializer
)
from .tasks import add as celery_add  # Import your Celery task
from celery.result import AsyncResult

class SanareSomaAPITests(TestCase):

# Removed the misplaced and incorrect line

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'test@example.com',
            'gender': 'male',
            'height': 180.0,
            'weight': 75.0,
            'dateofbirth': date(1990, 1, 15)
        }
        self.goal_data = {
            'userID': 1,
            'goaltype': 'weight_loss',
            'goalvalue': 70.0,
            'startdate': date(2023, 1, 1),
            'enddate': date(2023, 3, 31)
        }
        self.activity_data = {
            'activitydate': date(2023, 4, 1),
            'starttime': time(9, 0, 0),
            'endtime': time(10, 0, 0),
            'activitytype': 'running'
        }
        self.routine_data = {'activityID': 1}
        self.food_data = {
            'FoodName': 'Apple',
            'servingsize': 1.0,
            'servingunit': 'piece',
            'calories': 95.0,
            'protein': 0.5,
            'carbohydrates': 25.0,
            'fat': 0.3,
            'sodium': 1.0
        }
        self.meal_data = {
            'nutritionID': 1,
            'mealdate': date(2023, 4, 1),
            'mealtime': time(12, 0, 0),
            'mealtype': 'lunch'
        }
        self.nutrition_data = {'mealID': 1}
        self.client_data = {'userID': 1}
        self.professional_data = {
            'username': 'testprof',
            'password': 'profpass',
            'email': 'prof@example.com',
            'profession': 'nutritionist',
            'specialty': 'weight management'
        }

    def test_create_activity_invalid_duration(self):
        url = reverse('activity-list')
        invalid_activity_data = {
            'activitydate': date(2025, 4, 15),
            'starttime': time(10, 0, 0),
            'endtime': time(9, 30, 0),  # End time before start time
            'activitytype': 'yoga'
        }
        response = self.client.post(url, invalid_activity_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('starttime', response.data) # Assuming your serializer validates this

def test_user_achieves_weight_loss_goal(self):
    user = User.objects.create(**self.user_data, weight=78.0, height=170.0)
    goal = Goal.objects.create(userID=user.id, goaltype='weight_loss', goalvalue=75.0,
                               startdate=date(2025, 4, 1), enddate=date(2025, 5, 1))
    user.weight = 74.5
    user.save()
    # Assuming you have a method in your User model or a view to check goal achievement
    url = reverse('check-goal-achievement', args=[user.id, goal.id])
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertTrue(response.data['achieved'])


    def test_create_user(self):
        url = reverse('user-list')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_get_user(self):
        user = User.objects.create(**self.user_data)
        url = reverse('user-detail', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_create_goal(self):
        user = User.objects.create(**self.user_data)
        self.goal_data['userID'] = user.id
        url = reverse('goal-list')
        response = self.client.post(url, self.goal_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Goal.objects.count(), 1)
        self.assertEqual(Goal.objects.get().goaltype, 'weight_loss')

    def test_calculate_bmi(self):
        """
        Test a custom API endpoint to calculate BMI.
        """
        user = User.objects.create(**self.user_data)
        url = reverse('calculate-bmi', args=[user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expected BMI = weight (kg) / height (m)^2
        # 75 kg / (1.8 m)^2 = 75 / 3.24 = 23.15 (approximately)
        self.assertAlmostEqual(response.data['bmi'], 23.15, places=2)

    @patch('apis.tasks.add.delay')
    def test_add_numbers_celery(self, mock_delay):
        """
        Test an API endpoint that triggers a Celery task.
        """
        url = reverse('add-numbers')
        response = self.client.post(url, {'x': 5, 'y': 10}, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn('task_id', response.data)
        mock_delay.assert_called_once_with(5, 10)

    def test_get_task_status(self):
        """
        Test an API endpoint to get the status of a Celery task.
        """
        # Simulate a task ID
        mock_task_id = 'fake_task_id'
        with patch('celery.result.AsyncResult.ready', return_value=True), \
             patch('celery.result.AsyncResult.successful', return_value=True), \
             patch('celery.result.AsyncResult.get', return_value=15):
            url = reverse('task-status', args=[mock_task_id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['status'], 'SUCCESS')
            self.assertEqual(response.data['result'], 15)

        with patch('celery.result.AsyncResult.ready', return_value=False):
            url = reverse('task-status', args=[mock_task_id])
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['status'], 'PENDING')
            self.assertNotIn('result', response.data)

# Extend your Django models (if you haven't already in models.py)
from django.db import models

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

    def calculate_bmi(self):
        if self.height > 0:
            height_in_meters = self.height / 100.0
            return self.weight / (height_in_meters ** 2)
        return None

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

# Extend your Django serializers (if you haven't already in serializers.py)
from rest_framework import serializers

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

# Extend your Django views (in views.py)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from .tasks import add as celery_add  # Import your Celery task
from celery.result import AsyncResult

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['get'])
    def calculate_bmi(self, request, pk=None):
        """
        Calculates the Body Mass Index for a specific user.
        """
        try:
            user = self.get_object()
            bmi = user.calculate_bmi()
            if bmi is not None:
                return Response({'bmi': f'{bmi:.2f}'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Could not calculate BMI due to missing or zero height.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

from rest_framework.decorators import api_view
@api_view(['POST'])
def add_numbers(request):
    """
    Triggers a Celery task to add two numbers.
    """
    x = request.data.get('x')
    y = request.data.get('y')
    if x is not None and y is not None:
        task = celery_add.delay(x, y)
        return Response({'task_id': task.id}, status=status.HTTP_202_ACCEPTED)
    return Response({'error': 'Please provide both x and y.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_task_status(request, task_id):
    """
    Retrieves the status and result of a Celery task.
    """
    task_result = AsyncResult(task_id)
    result = {
        'status': task_result.status,
        'ready': task_result.ready(),
        'successful': task_result.successful(),
        'failed': task_result.failed(),
    }
    if task_result.ready():
        result['result'] = task_result.get()
    return Response(result, status=status.HTTP_200_OK)

# Extend your Django urls (in urls.py)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, add_numbers, get_task_status

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'goals', viewsets.ModelViewSet(queryset=Goal.objects.all(), serializer_class=GoalSerializer))
router.register(r'activities', viewsets.ModelViewSet(queryset=Activity.objects.all(), serializer_class=ActivitySerializer))
router.register(r'routines', viewsets.ModelViewSet(queryset=Routine.objects.all(), serializer_class=RoutineSerializer))
router.register(r'foods', viewsets.ModelViewSet(queryset=Food.objects.all(), serializer_class=FoodSerializer))
router.register(r'meals', viewsets.ModelViewSet(queryset=Meal.objects.all(), serializer_class=MealSerializer))
router.register(r'nutritions', viewsets.ModelViewSet(queryset=Nutrition.objects.all(), serializer_class=NutritionSerializer))
router.register(r'clients', viewsets.ModelViewSet(queryset=Client.objects.all(), serializer_class=ClientSerializer))
router.register(r'professionals', viewsets.ModelViewSet(queryset=Professionals.objects.all(), serializer_class=ProfessionalsSerializer))

urlpatterns = [
    path('', include(router.urls)),
    path('users/<int:pk>/calculate_bmi/', UserViewSet.as_view({'get': 'calculate_bmi'}), name='calculate-bmi'),
    path('add/', add_numbers, name='add-numbers'),
    path('tasks/<str:task_id>/status/', get_task_status, name='task-status'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]

# Ensure you have your Celery task defined in tasks.py
from celery import Celery

app = Celery('apis', broker='redis://localhost:6379/0')

@app.task
def add(x, y):
    return x + y