from django import forms
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404
from .models import Goal, UserProfile, Professional
from .tasks import notify_client_about_new_goal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from SonareSoma.repositories import ProfessionalRepository, UserProfileRepository

class GoalForm(forms.ModelForm):
    client = forms.ModelChoiceField(queryset=UserProfile.objects.none(), required=True)

    class Meta:
        model = Goal
        fields = ['goaltype', 'goalvalue', 'startdate', 'enddate', 'client']

    def __init__(self, *args, **kwargs):
        professional = kwargs.pop('professional', None)
        super().__init__(*args, **kwargs)
        if professional:
            self.fields['client'].queryset = ProfessionalRepository.get_clients_for_professional(professional)

    def clean_client(self):
        client = self.cleaned_data.get('client')
        if not client:
            raise forms.ValidationError("Client is required")
        return client

class ClientGoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['goaltype', 'goalvalue', 'startdate', 'enddate']

def set_goal_for_client(request):
    professional = ProfessionalRepository.get_professional_by_user(request.user)
    if not professional:
        raise Http404("Professional not found")

    clients = ProfessionalRepository.get_clients_for_professional(professional)

    if request.method == 'POST':
        form = GoalForm(request.POST, professional=professional)
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
        form = GoalForm(professional=professional)

    return render(request, 'set_goal.html', {'form': form, 'clients': clients})

class GoalViewTests(TestCase):
    def setUp(self):
        self.professional_user = User.objects.create_user(username='professional', password='password')
        self.client_user = User.objects.create_user(username='client', password='password')
        self.professional = Professional.objects.create(user=self.professional_user)
        self.client_profile = UserProfile.objects.create(user=self.client_user)
        self.professional.clients.add(self.client_profile)

    def test_set_goal_for_client(self):
        self.client.login(username='professional', password='password')
        response = self.client.post(reverse('set_goal'), {
            'goaltype': 'Weight Loss',
            'goalvalue': 10,
            'startdate': '2025-05-01',
            'enddate': '2025-06-01',
            'client': self.client_profile.id,
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Goal.objects.filter(client=self.client_profile).exists())
