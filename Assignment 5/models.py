from django.contrib import admin
# include necessary libraries
from django.urls import path, include
 
urlpatterns = [
    path('admin/', admin.site.urls),
    # add apis urls
    path('', include("apis.urls"))]


#Create a model
#To demonstrate, create api in python django and using an API, let’s create a model named “SanareSoma"”. In apis/models.py

from django.db import models
from django.contrib import admin
 
 
class SanareSoma(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
 
def __str__(self):
    return self.title


# Run the following command in the terminal to create migrations:
# python manage.py makemigrations

# Run the following command in the terminal to apply migrations:
# python manage.py migrate

# Run the following command in the terminal to start the development server:
# python manage.py runserver