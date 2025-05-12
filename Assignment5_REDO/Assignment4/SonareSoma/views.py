from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Professional, Goal, Activity, UserProfile
from .serializers import ProfessionalSerializer, GoalSerializer, ActivitySerializer, UserProfileSerializer
from .forms import GoalForm, ClientGoalForm
from .tasks import notify_client_about_new_goal
from .repositories import ProfessionalRepository, UserProfileRepository, GoalRepository

class IsProfessional(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'professional_profile')  # Check if the user is a professional

class ProfessionalViewSet(viewsets.ModelViewSet):
    queryset = Professional.objects.all()
    serializer_class = ProfessionalSerializer

class GoalViewSet(viewsets.ModelViewSet):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, IsProfessional]

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

def set_goal_for_client(request):
    try:
        professional = Professional.objects.get(PTUser=request.user)
    except Professional.DoesNotExist:
        messages.error(request, "Professional not found")
        return redirect('home')  # Redirect to a safe page

    clients = ProfessionalRepository.get_clients_for_professional(professional)

    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.client = UserProfileRepository.get_user_profile_by_id(request.POST['client'])
            if not goal.client:
                messages.error(request, "Client not found")
                return redirect('set_goal')
            goal.professional = professional
            goal.save()
            notify_client_about_new_goal.delay(professional.id, goal.client.id, goal.id)
            messages.success(request, "Goal successfully set for the client!")
            return redirect('set_goal')
    else:
        form = GoalForm()

    return render(request, 'set_goal.html', {'form': form, 'clients': clients})

def client_input_goal(request):
    if request.method == 'POST':
        form = ClientGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.client = UserProfileRepository.get_user_profile_by_user(request.user)
            if not goal.client:
                messages.error(request, "Client profile not found")
                return redirect('client_input_goal')
            goal.save()
            return redirect('goal_success')  # Redirect to a success page
    else:
        form = ClientGoalForm()
    return render(request, 'client_input_goal.html', {'form': form})