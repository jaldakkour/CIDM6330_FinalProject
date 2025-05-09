# Create your models here.
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User as AuthUser


class SanareSoma(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # Store hashed passwords!
    email = models.EmailField()
    gender = models.CharField(max_length=10, blank=True, null=True)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    dateofbirth = models.DateField(blank=True, null=True)
    goal = models.ForeignKey('Goal', on_delete=models.SET_NULL, blank=True, null=True)  # Foreign Key
    routine = models.ForeignKey('Routine', on_delete=models.SET_NULL, blank=True, null=True) # FK
    nutrition = models.ForeignKey('Nutrition', on_delete=models.SET_NULL, blank=True, null=True) # FK
    professional = models.ForeignKey('Professional', on_delete=models.SET_NULL, blank=True, null=True) # FK

    def __str__(self):
        return self.username

class Professional(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)  # Store hashed passwords!
    email = models.EmailField()
    profession = models.CharField(max_length=255, blank=True, null=True)
    specialty = models.CharField(max_length=255, blank=True, null=True)
    routine = models.ForeignKey('Routine', on_delete=models.SET_NULL, blank=True, null=True) #FK
    nutrition = models.ForeignKey('Nutrition', on_delete=models.SET_NULL, blank=True, null=True) #FK


    def __str__(self):
        return self.username


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #FK
    goaltype = models.CharField(max_length=255)
    goalvalue = models.FloatField()
    startdate = models.DateField()
    enddate = models.DateField()

    def __str__(self):
        return f"Goal {self.id} for User {self.user.username}"


class Activity(models.Model):
    activitydate = models.DateField()
    starttime = models.TimeField()
    endtime = models.TimeField()
    activitytype = models.CharField(max_length=255)


    def __str__(self):
        return f"Activity {self.id} - {self.activitytype} on {self.activitydate}"



class Routine(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE) #FK

    def __str__(self):
        return f"Routine {self.id}"


class Food(models.Model):
    FoodName = models.CharField(max_length=255)
    FoodBrand = models.CharField(max_length=255, blank=True, null=True)
    servingsize = models.FloatField()
    servingunit = models.CharField(max_length=255)
    calories = models.FloatField()
    protein = models.FloatField()
    carbohydrates = models.FloatField()
    fat = models.FloatField()
    sodium = models.FloatField()

    def __str__(self):
        return self.FoodName


class Meal(models.Model):
    nutrition = models.ForeignKey('Nutrition', on_delete=models.CASCADE) #FK
    mealdate = models.DateField()
    mealtime = models.TimeField()
    mealtype = models.CharField(max_length=255)

    def __str__(self):
        return f"Meal {self.id} on {self.mealdate}"


class Nutrition(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE) #FK


    def __str__(self):
        return f"Nutrition {self.id}"


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #FK

    def __str__(self):
        return f"Client {self.id}"
