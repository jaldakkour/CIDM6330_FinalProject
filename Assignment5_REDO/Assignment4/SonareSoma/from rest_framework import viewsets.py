from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Professional
from .serializers import ProfessionalSerializer  # Import the serializer

class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer

    @action(detail=True, methods=['get'])
    def weekly_summary(self, request, pk=None):
        professional = self.get_object()
        # Custom logic to generate a summary
        summary = {"message": f"Weekly summary for {professional.user.username}"}
        return Response(summary)