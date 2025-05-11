from celery import shared_task
from django.utils import timezone
from .models import Routine, UserProfile, Professional
from django.db import models
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_daily_routine_reminder():
    today = timezone.now().date()
    for routine in Routine.objects.all():
        users = routine.user_profiles.all()  # Assuming Routine is linked to UserProfile
        for user in users:
            subject = "Today's Routine Reminder"
            message = f"Hi {user.user.username},\n\nHere are your activities for today:\n"
            activities = routine.activities.filter(activitydate=today)
            if activities.exists():
                activity_list = "\n".join([f"- {activity.activitytype} at {activity.starttime}" for activity in activities])
                message += f"{activity_list}\n\nStay consistent and achieve your goals!"
            else:
                message += "No activities scheduled for today. Enjoy your rest day!"
            from_email = 'your_email@example.com'
            recipient_list = [user.user.email]
            send_mail(subject, message, from_email, recipient_list)
            print(f"Sent daily routine reminder to {user.user.email}")

@shared_task
def send_weekly_goal_summary():
    today = timezone.now().date()
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)

    for user in UserProfile.objects.all():
        goals = user.goal_set.filter(startdate__lte=end_of_week, enddate__gte=start_of_week)
        if goals.exists():
            subject = "Your Weekly Goal Progress Summary"
            message = f"Hi {user.user.username},\n\nHere's your progress for this week:\n"
            for goal in goals:
                progress = f"- {goal.goaltype}: {goal.goalvalue} (Target: {goal.goalvalue})"
                message += f"{progress}\n"
            message += "\nKeep up the great work!"
            from_email = 'your_email@example.com'
            recipient_list = [user.user.email]
            send_mail(subject, message, from_email, recipient_list)
            print(f"Sent weekly goal summary to {user.user.email}")

@shared_task
def send_missed_routine_notification():
    yesterday = timezone.now().date() - timezone.timedelta(days=1)
    for routine in Routine.objects.all():
        users = routine.user_profiles.all()
        for user in users:
            missed_activities = routine.activities.filter(activitydate=yesterday, endtime__lt=timezone.now().time())
            if missed_activities.exists():
                subject = "Missed Routine Notification"
                message = f"Hi {user.user.username},\n\nYou missed the following activities yesterday:\n"
                activity_list = "\n".join([f"- {activity.activitytype} at {activity.starttime}" for activity in missed_activities])
                message += f"{activity_list}\n\nDon't worry, you can get back on track today!"
                from_email = 'your_email@example.com'
                recipient_list = [user.user.email]
                send_mail(subject, message, from_email, recipient_list)
                print(f"Sent missed routine notification to {user.user.email}")

@shared_task
def send_daily_meal_plan_reminder():
    today = timezone.now().date()
    for user in UserProfile.objects.all():
        if user.nutrition:
            subject = "Daily Meal Plan Reminder"
            message = f"Hi {user.user.username},\n\nDon't forget to log your meals for today!\n"
            message += "Following your meal plan is key to achieving your nutrition goals.\n\n"
            message += "Stay consistent and healthy!"
            from_email = 'your_email@example.com'
            recipient_list = [user.user.email]
            send_mail(subject, message, from_email, recipient_list)
            print(f"Sent daily meal plan reminder to {user.user.email}")

@shared_task
def send_motivational_message():
    motivational_quotes = [
        "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.",
        "Success is the sum of small efforts, repeated day in and day out.",
        "The difference between a successful person and others is not a lack of strength, but a lack of will.",
        "Your body can stand almost anything. It’s your mind that you have to convince.",
    ]
    today = timezone.now().date()
    for user in UserProfile.objects.all():
        subject = "Stay Motivated!"
        message = f"Hi {user.user.username},\n\nHere's a motivational quote for you:\n\n"
        message += f"\"{motivational_quotes[today.weekday() % len(motivational_quotes)]}\"\n\n"
        message += "Keep pushing toward your goals!"
        from_email = 'your_email@example.com'
        recipient_list = [user.user.email]
        send_mail(subject, message, from_email, recipient_list)
        print(f"Sent motivational message to {user.user.email}")

@shared_task
def send_client_progress_report():
    for professional in Professional.objects.all():
        clients = professional.clients.all()
        if clients.exists():
            subject = "Weekly Client Progress Report"
            message = f"Hi {professional.user.username},\n\nHere's the progress report for your clients this week:\n"
            for client in clients:
                message += f"- {client.user.username}: {client.goal.goaltype} (Target: {client.goal.goalvalue})\n"
            message += "\nKeep supporting your clients to achieve their goals!"
            from_email = 'your_email@example.com'
            recipient_list = [professional.user.email]
            send_mail(subject, message, from_email, recipient_list)
            print(f"Sent client progress report to {professional.user.email}")

@shared_task
def send_weekly_professional_summary():
    from django.utils.timezone import now
    today = now().date()
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)

    for professional in Professional.objects.all():
        subject = "Weekly Summary of Goals Set for Clients"
        message = f"Hi {professional.user.username},\n\nHere is a summary of the goals you have set for your clients this week:\n\n"

        for client in professional.clients.all():
            goals = client.goals.filter(startdate__range=(start_of_week, end_of_week))
            if goals.exists():
                message += f"Client: {client.user.username}\n"
                for goal in goals:
                    message += f"- {goal.goaltype}: {goal.goalvalue} (Start: {goal.startdate}, End: {goal.enddate})\n"
                message += "\n"

        message += "Keep supporting your clients to achieve their goals!"
        from_email = 'your_email@example.com'
        recipient_list = [professional.user.email]
        send_mail(subject, message, from_email, recipient_list)
        print(f"Sent weekly summary to professional {professional.user.email}")

@shared_task
def backup_database():
    from django.core.management import call_command
    import os
    backup_dir = "/path/to/backup/directory"
    os.makedirs(backup_dir, exist_ok=True)
    backup_file = os.path.join(backup_dir, f"db_backup_{timezone.now().strftime('%Y%m%d%H%M%S')}.json")
    with open(backup_file, 'w') as f:
        call_command('dumpdata', stdout=f)
    print(f"Database backup saved to {backup_file}")

@shared_task
def send_inactivity_reminder():
    one_week_ago = timezone.now().date() - timezone.timedelta(days=7)
    for user in UserProfile.objects.all():
        last_activity = user.routine.activities.order_by('-activitydate').first()
        if not last_activity or last_activity.activitydate < one_week_ago:
            subject = "We Miss You!"
            message = f"Hi {user.user.username},\n\nWe noticed you haven't logged any activities recently. "
            message += "Remember, consistency is key to achieving your goals. Let's get back on track today!"
            from_email = 'your_email@example.com'
            recipient_list = [user.user.email]
            send_mail(subject, message, from_email, recipient_list)
            print(f"Sent inactivity reminder to {user.user.email}")

@shared_task
def send_weekly_nutrition_summary():
    today = timezone.now().date()
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)

    for user in UserProfile.objects.all():
        if user.nutrition:
            meals = user.nutrition.meals.filter(mealdate__range=(start_of_week, end_of_week))
            if meals.exists():
                subject = "Your Weekly Nutrition Summary"
                message = f"Hi {user.user.username},\n\nHere's your nutrition summary for the week:\n"
                total_calories = 0
                total_protein = 0
                total_carbs = 0
                total_fat = 0

                for meal in meals:
                    for food in meal.foods.all():
                        total_calories += food.calories
                        total_protein += food.protein
                        total_carbs += food.carbohydrates
                        total_fat += food.fat

                message += f"- Total Calories: {total_calories}\n"
                message += f"- Total Protein: {total_protein}g\n"
                message += f"- Total Carbohydrates: {total_carbs}g\n"
                message += f"- Total Fat: {total_fat}g\n"
                message += "\nKeep tracking your meals to stay on top of your nutrition goals!"
                from_email = 'your_email@example.com'
                recipient_list = [user.user.email]
                send_mail(subject, message, from_email, recipient_list)
                print(f"Sent weekly nutrition summary to {user.user.email}")

@shared_task
def send_monthly_progress_report():
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)

    for user in UserProfile.objects.all():
        subject = "Your Monthly Progress Report"
        message = f"Hi {user.user.username},\n\nHere's your progress for the month:\n"

        # Goals
        goals = user.goal_set.filter(startdate__lte=end_of_month, enddate__gte=start_of_month)
        if goals.exists():
            message += "\nGoals:\n"
            for goal in goals:
                message += f"- {goal.goaltype}: {goal.goalvalue} (Target: {goal.goalvalue})\n"

        # Routines
        routines = user.routine.activities.filter(activitydate__range=(start_of_month, end_of_month))
        if routines.exists():
            message += "\nRoutines Completed:\n"
            for routine in routines:
                message += f"- {routine.activitytype} on {routine.activitydate}\n"

        # Nutrition
        if user.nutrition:
            meals = user.nutrition.meals.filter(mealdate__range=(start_of_month, end_of_month))
            if meals.exists():
                total_calories = sum(food.calories for meal in meals for food in meal.foods.all())
                message += f"\nTotal Calories Consumed: {total_calories}\n"

        message += "\nKeep up the great work and stay consistent!"
        from_email = 'your_email@example.com'
        recipient_list = [user.user.email]
        send_mail(subject, message, from_email, recipient_list)
        print(f"Sent monthly progress report to {user.user.email}")

@shared_task
def notify_goal_achievement():
    today = timezone.now().date()
    for user in UserProfile.objects.all():
        achieved_goals = user.goal_set.filter(enddate__lte=today, goalvalue__lte=100)  # Assuming goalvalue tracks progress
        for goal in achieved_goals:
            subject = "Congratulations on Achieving Your Goal!"
            message = f"Hi {user.user.username},\n\nCongratulations on achieving your goal:\n"
            message += f"- {goal.goaltype}: {goal.goalvalue}\n"
            message += "\nYour hard work and dedication have paid off. Keep setting new goals and pushing forward!"
            from_email = 'your_email@example.com'
            recipient_list = [user.user.email]
            send_mail(subject, message, from_email, recipient_list)
            print(f"Sent goal achievement notification to {user.user.email}")

@shared_task
def notify_client_of_message(professional_id, client_id, message_content):
    from .models import Professional, UserProfile

    try:
        professional = Professional.objects.get(id=professional_id)
        client = UserProfile.objects.get(id=client_id)

        subject = "New Message from Your Professional"
        message = f"Hi {client.user.username},\n\nYou have received a new message from {professional.user.username}:\n\n"
        message += f"\"{message_content}\"\n\n"
        message += "Please log in to your account to respond or view more details."
        from_email = 'your_email@example.com'
        recipient_list = [client.user.email]
        send_mail(subject, message, from_email, recipient_list)
        print(f"Sent message notification to client {client.user.email}")
    except Professional.DoesNotExist:
        print(f"Professional with ID {professional_id} does not exist.")
    except UserProfile.DoesNotExist:
        print(f"Client with ID {client_id} does not exist.")

@shared_task
def notify_professional_of_message(client_id, professional_id, message_content):
    from .models import Professional, UserProfile

    try:
        client = UserProfile.objects.get(id=client_id)
        professional = Professional.objects.get(id=professional_id)

        subject = "New Message from Your Client"
        message = f"Hi {professional.user.username},\n\nYou have received a new message from {client.user.username}:\n\n"
        message += f"\"{message_content}\"\n\n"
        message += "Please log in to your account to respond or view more details."
        from_email = 'your_email@example.com'
        recipient_list = [professional.user.email]
        send_mail(subject, message, from_email, recipient_list)
        print(f"Sent message notification to professional {professional.user.email}")
    except UserProfile.DoesNotExist:
        print(f"Client with ID {client_id} does not exist.")
    except Professional.DoesNotExist:
        print(f"Professional with ID {professional_id} does not exist.")

@shared_task
def send_monthly_engagement_report():
    from .models import Professional, Message  # Assuming you have a Message model
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)

    for professional in Professional.objects.all():
        messages_sent = Message.objects.filter(sender=professional.user, timestamp__range=(start_of_month, end_of_month)).count()
        messages_received = Message.objects.filter(recipient=professional.user, timestamp__range=(start_of_month, end_of_month)).count()

        subject = "Monthly Engagement Report"
        message = f"Hi {professional.user.username},\n\nHere is your engagement report for the month:\n"
        message += f"- Messages Sent: {messages_sent}\n"
        message += f"- Messages Received: {messages_received}\n"
        message += "\nKeep engaging with your clients to help them achieve their goals!"
        from_email = 'your_email@example.com'
        recipient_list = [professional.user.email]
        send_mail(subject, message, from_email, recipient_list)
        print(f"Sent monthly engagement report to professional {professional.user.email}")

@shared_task
def send_monthly_nutrition_insights():
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)

    for user in UserProfile.objects.all():
        if user.nutrition:
            meals = user.nutrition.meals.filter(mealdate__range=(start_of_month, end_of_month))
            if meals.exists():
                total_calories = sum(food.calories for meal in meals for food in meal.foods.all())
                avg_calories = total_calories / meals.count()
                subject = "Monthly Nutrition Insights"
                message = f"Hi {user.user.username},\n\nHere are your nutrition insights for the month:\n"
                message += f"- Total Calories Consumed: {total_calories}\n"
                message += f"- Average Daily Calories: {avg_calories:.2f}\n"
                message += "\nKeep tracking your meals to maintain a balanced diet!"
                from_email = 'your_email@example.com'
                recipient_list = [user.user.email]
                send_mail(subject, message, from_email, recipient_list)
                print(f"Sent monthly nutrition insights to {user.user.email}")

@shared_task
def send_professional_feedback_request():
    for professional in Professional.objects.all():
        for client in professional.clients.all():
            subject = "We Value Your Feedback!"
            message = f"Hi {client.user.username},\n\nWe'd love to hear your thoughts about your experience with {professional.user.username}.\n"
            message += "Your feedback helps us improve and provide the best support possible.\n\n"
            message += "Please log in to your account to leave feedback."
            from_email = 'your_email@example.com'
            recipient_list = [client.user.email]
            send_mail(subject, message, from_email, recipient_list)
            print(f"Sent feedback request to client {client.user.email}")

@shared_task
def send_routine_completion_certificate(user_id, routine_id):
    from .models import Routine, UserProfile

    try:
        user = UserProfile.objects.get(id=user_id)
        routine = Routine.objects.get(id=routine_id)

        subject = "Congratulations on Completing Your Routine!"
        message = f"Hi {user.user.username},\n\nCongratulations on completing the routine \"{routine.name}\"!\n"
        message += "Your dedication and hard work have paid off. Keep striving for greatness!\n\n"
        message += "Attached is your certificate of completion."
        from_email = 'your_email@example.com'
        recipient_list = [user.user.email]

        # Generate and attach a certificate (placeholder logic)
        # You can use a library like ReportLab or WeasyPrint to generate a PDF certificate.
        # For now, this is just a placeholder.
        send_mail(subject, message, from_email, recipient_list)
        print(f"Sent routine completion certificate to {user.user.email}")
    except UserProfile.DoesNotExist:
        print(f"User with ID {user_id} does not exist.")
    except Routine.DoesNotExist:
        print(f"Routine with ID {routine_id} does not exist.")

@shared_task
def send_monthly_client_retention_report():
    today = timezone.now().date()
    start_of_month = today.replace(day=1)
    end_of_month = (start_of_month + timezone.timedelta(days=32)).replace(day=1) - timezone.timedelta(days=1)

    for professional in Professional.objects.all():
        total_clients = professional.clients.count()
        active_clients = professional.clients.filter(
            routine__activities__activitydate__range=(start_of_month, end_of_month)
        ).distinct().count()

        retention_rate = (active_clients / total_clients) * 100 if total_clients > 0 else 0

        subject = "Monthly Client Retention Report"
        message = f"Hi {professional.user.username},\n\nHere's your client retention report for the month:\n"
        message += f"- Total Clients: {total_clients}\n"
        message += f"- Active Clients: {active_clients}\n"
        message += f"- Retention Rate: {retention_rate:.2f}%\n\n"
        message += "Keep engaging with your clients to maintain high retention rates!"
        from_email = 'your_email@example.com'
        recipient_list = [professional.user.email]
        send_mail(subject, message, from_email, recipient_list)
        print(f"Sent client retention report to {professional.user.email}")

@shared_task
def send_weekly_meal_plan_suggestions():
    for user in UserProfile.objects.all():
        if user.nutrition:
            subject = "Weekly Meal Plan Suggestions"
            message = f"Hi {user.user.username},\n\nHere are some meal suggestions for the week based on your nutrition goals:\n"
            message += "- Breakfast: Oatmeal with fresh fruits and nuts.\n"
            message += "- Lunch: Grilled chicken with quinoa and steamed vegetables.\n"
            message += "- Dinner: Baked salmon with sweet potatoes and a side salad.\n"
            message += "- Snacks: Greek yogurt, almonds, or a protein bar.\n\n"
            message += "Log in to your account to customize your meal plan!"
            from_email = 'your_email@example.com'
            recipient_list = [user.user.email]
            send_mail(subject, message, from_email, recipient_list)
            print(f"Sent meal plan suggestions to {user.user.email}")

@shared_task
def validate_goal_input(goal_id):
    from .models import Goal
    try:
        goal = Goal.objects.get(id=goal_id)
        if goal.goalvalue <= 0:
            print(f"Invalid goal value for goal ID {goal_id}")
        else:
            print(f"Goal ID {goal_id} is valid")
    except Goal.DoesNotExist:
        print(f"Goal with ID {goal_id} does not exist")

@shared_task
def send_weekly_activity_leaderboard():
    today = timezone.now().date()
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)

    leaderboard = UserProfile.objects.annotate(
        activity_count=models.Count('routine__activities', filter=models.Q(routine__activities__activitydate__range=(start_of_week, end_of_week)))
    ).order_by('-activity_count')[:10]

    for user in UserProfile.objects.all():
        subject = "Weekly Activity Leaderboard"
        message = f"Hi {user.user.username},\n\nHere are the top performers for this week:\n\n"
        for rank, profile in enumerate(leaderboard, start=1):
            message += f"{rank}. {profile.user.username} - {profile.activity_count} activities\n"
        message += "\nKeep pushing yourself to climb the leaderboard next week!"
        from_email = 'your_email@example.com'
        recipient_list = [user.user.email]
        send_mail(subject, message, from_email, recipient_list)
        print(f"Sent weekly leaderboard to {user.user.email}")

@shared_task
def notify_client_about_new_goal(professional_id, client_id, goal_id):
    try:
        # Task logic here
        pass
    except Exception as e:
        logger.error(f"Error in notify_client_about_new_goal: {e}")

@shared_task
def notify_professional_about_client_goal(client_id, goal_id):
    from .models import Professional, UserProfile, Goal

    try:
        client = UserProfile.objects.get(id=client_id)
        goal = Goal.objects.get(id=goal_id)
        professional = client.professional  # Assuming a `professional` field links the client to their professional

        subject = "New Goal Submitted by Your Client"
        message = f"Hi {professional.user.username},\n\nYour client, {client.user.username}, has submitted a new goal:\n\n"
        message += f"- Goal Type: {goal.goaltype}\n"
        message += f"- Target Value: {goal.goalvalue}\n"
        message += f"- Start Date: {goal.startdate}\n"
        message += f"- End Date: {goal.enddate}\n\n"
        message += "Log in to your account to view more details."
        from_email = 'your_email@example.com'
        recipient_list = [professional.user.email]
        send_mail(subject, message, from_email, recipient_list)
        print(f"Sent new goal notification to professional {professional.user.email}")
    except UserProfile.DoesNotExist:
        print(f"Client with ID {client_id} does not exist.")
    except Goal.DoesNotExist:
        print(f"Goal with ID {goal_id} does not exist.")

@shared_task
def send_weekly_professional_goal_summary():
    today = timezone.now().date()
    start_of_week = today - timezone.timedelta(days=today.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)

    for professional in Professional.objects.all():
        subject = "Weekly Summary of Goals Set for Clients"
        message = f"Hi {professional.user.username},\n\nHere is a summary of the goals you have set for your clients this week:\n\n"

        for client in professional.clients.all():
            goals = client.goals.filter(startdate__range=(start_of_week, end_of_week))
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


import logging
from celery import shared_task

logger = logging.getLogger(__name__)

@shared_task
def notify_client_about_new_goal(professional_id, client_id, goal_id):
    try:
        # Task logic here
        pass
    except Exception as e:
        logger.error(f"Error in notify_client_about_new_goal: {e}")
