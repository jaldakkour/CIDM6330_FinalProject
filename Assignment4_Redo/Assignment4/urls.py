from django.urls import path, include
from rest_framework import routers
from ..api1 import views

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api1.urls')),  
]

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'professionals', views.ProfessionalViewSet)
router.register(r'goals', views.GoalViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'routines', views.RoutineViewSet)
router.register(r'foods', views.FoodViewSet)
router.register(r'meals', views.MealViewSet)
router.register(r'nutritions', views.NutritionViewSet)
router.register(r'clients', views.ClientViewSet)


urlpatterns = [
    path('api/', include(router.urls)), 
]
