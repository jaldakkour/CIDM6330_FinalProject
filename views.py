#Creating a Viewset
#To render data into frontend, and handle requests from user, we need to create a view. In Django REST Framework, we call these as viewsets, so let’s create a view in apis/views.py

# import viewsets
from rest_framework import viewsets
 
# import local data
from .serializers import SanareSomaSerializer
from .models import SonareSoma
 
# create a viewset
 
 
class GeeksViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = SonareSoma.objects.all()
 
    # specify serializer to be used
    serializer_class = SanareSomaSerializer