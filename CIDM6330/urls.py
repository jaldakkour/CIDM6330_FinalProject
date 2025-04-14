from django.urls import include, path
from rest_framework import routers
from .views import SanareSomaViewSet, SanareSomaViewSet  # Corrected import

router = routers.DefaultRouter()
router.register(r'SanareSoma', SanareSomaViewSet)  # Register the correct viewset

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', include('admin.site.urls')),
]

#Navigate to the directory where manage.py is located and run the following command:
# python manage.py runserver    

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

class SanareSomaViewSet(ViewSet):
    def list(self, request):
        return Response({"message": "SanareSomaViewSet is working!"})
    
    