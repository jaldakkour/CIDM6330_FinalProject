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

class IsProfess