from django.urls import path
from .views import set_goal_for_client, client_input_goal
from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from .repositories import ProfessionalRepository, UserProfileRepository

urlpatterns = [
    path('set-goal/', set_goal_for_client, name='set_goal'),
    path('input-goal/', client_input_goal, name='client_input_goal'),
]

@shared_task
def send_weekly_professional_goal_summary():
    today = timezone.now().date()
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)

    for professional in ProfessionalRepository.get_all_professionals():
        subject = "Weekly Summary of Goals Set for Clients"
        message = f"Hi {professional.user.username},\n\nHere is a summary of the goals you have set for your clients this week:\n\n"

        for client in ProfessionalRepository.get_clients_for_professional(professional):
            goals = UserProfileRepository.get_goals_for_client(client, start_of_week, end_of_week)
            if goals.exists():
                message += f"Client: {client.user.username}\n"
                for goal in goals:
                    message += f"- {goal.goaltype}: {goal.goalvalue} (Start: {goal.startdate}, End: {goal.enddate})\n"
                message += "\n"

        message += "Keep supporting your clients to achieve their goals!"
        from_email = 'your_email@example.com'
        recipient_list = [professional.user.email]
        send_mail(subject, message, from_email, recipient_list)
        print(f"Sent weekly goal summary to professional {professional.user.email}")

from rest_framework.routers import DefaultRouter
from .views import GoalViewSet, UserProfileViewSet, ProfessionalViewSet

router = DefaultRouter()
router.register(r'goals', GoalViewSet)
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'professionals', ProfessionalViewSet)

urlpatterns = router.urls