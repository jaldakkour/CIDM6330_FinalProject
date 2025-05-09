from rest_framework import viewsets
 
from .serializers import SanareSomaSerializer
from .models import SonareSoma

class GeeksViewSet(viewsets.ModelViewSet):
    queryset = SonareSoma.objects.all()
    serializer_class = SanareSomaSerializer
