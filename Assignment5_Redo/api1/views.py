from rest_framework import viewsets
 
from .serializers import SanareSomaSerializer
from .models import SonareSoma

class GeeksViewSet(viewsets.ModelViewSet):
    queryset = SonareSoma.objects.all()
    serializer_class = SanareSomaSerializer
 
from django.http import HttpResponse
from .tasks import add, send_email_notification

def my_view(request):
    result = add.delay(5, 3)  # This doesn't block; the task runs in the background
    send_email_notification.delay(request.user.id, "Welcome!", "Thanks for joining our platform.")
    return HttpResponse(f"Task submitted! Task ID: {result.id}")
