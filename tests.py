from django.test import TestCase
from .tasks import notify_client_about_new_goal, send_weekly_professional_summary
from .models import Professional, UserProfile, Goal
from django.contrib.auth.models import User
from django.core import mail
from .serializers import GoalSerializer

class TaskTests(TestCase):
    def test_notify_client_about_new_goal(self):
        # Set up test data
        professional = Professional.objects.create(user=User.objects.create(username="professional"))
        client = UserProfile.objects.create(user=User.objects.create(username="client"))
        goal = Goal.objects.create(
            goaltype="Weight Loss",
            goalvalue=10,
            startdate="2025-01-01",
            enddate="2025-02-01",
            client=client,
            professional=professional,
        )

        # Call the task
        notify_client_about_new_goal(professional.id, client.id, goal.id)

        # Assertions (e.g., check email was sent)

    def test_notify_client_about_new_goal_email_content(self):
        # Set up test data
        professional = Professional.objects.create(user=User.objects.create(username="professional"))
        client = UserProfile.objects.create(user=User.objects.create(username="client", email="client@example.com"))
        goal = Goal.objects.create(
            goaltype="Weight Loss",
            goalvalue=10,
            startdate="2025-01-01",
            enddate="2025-02-01",
            client=client,
            professional=professional,
        )

        # Call the task
        notify_client_about_new_goal(professional.id, client.id, goal.id)

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Verify email content
        email = mail.outbox[0]
        self.assertEqual(email.subject, "New Goal Set by Your Professional")
        self.assertIn("Hi client,", email.body)
        self.assertIn("Your professional, professional,", email.body)
        self.assertIn("Goal Type: Weight Loss", email.body)
        self.assertIn("Target Value: 10", email.body)

    def test_notify_client_about_new_goal_missing_professional(self):
        # Set up test data
        client = UserProfile.objects.create(user=User.objects.create(username="client"))
        goal = Goal.objects.create(
            goaltype="Weight Loss",
            goalvalue=10,
            startdate="2025-01-01",
            enddate="2025-02-01",
            client=client,
            professional=None,  # No professional assigned
        )

        # Call the task
        with self.assertLogs("django", level="ERROR") as log:
            notify_client_about_new_goal(999, client.id, goal.id)  # Invalid professional ID
            self.assertIn("Professional with ID 999 does not exist.", log.output[0])

    def test_notify_client_about_new_goal_missing_client(self):
        # Set up test data
        professional = Professional.objects.create(user=User.objects.create(username="professional"))
        goal = Goal.objects.create(
            goaltype="Weight Loss",
            goalvalue=10,
            startdate="2025-01-01",
            enddate="2025-02-01",
            client=None,  # No client assigned
            professional=professional,
        )

        # Call the task
        with self.assertLogs("django", level="ERROR") as log:
            notify_client_about_new_goal(professional.id, 999, goal.id)  # Invalid client ID
            self.assertIn("Client with ID 999 does not exist.", log.output[0])

    def test_notify_client_about_new_goal_missing_goal(self):
        # Set up test data
        professional = Professional.objects.create(user=User.objects.create(username="professional"))
        client = UserProfile.objects.create(user=User.objects.create(username="client"))

        # Call the task
        with self.assertLogs("django", level="ERROR") as log:
            notify_client_about_new_goal(professional.id, client.id, 999)  # Invalid goal ID
            self.assertIn("Goal with ID 999 does not exist.", log.output[0])

class WeeklySummaryTaskTests(TestCase):
    def test_send_weekly_professional_summary(self):
        # Set up test data
        professional = Professional.objects.create(user=User.objects.create(username="professional", email="professional@example.com"))
        client = UserProfile.objects.create(user=User.objects.create(username="client"))
        professional.clients.add(client)
        Goal.objects.create(
            goaltype="Weight Loss",
            goalvalue=10,
            startdate="2025-01-01",
            enddate="2025-02-01",
            client=client,
            professional=professional,
        )

        # Call the task
        send_weekly_professional_summary()

        # Check that an email was sent
        from django.core import mail
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(email.subject, "Weekly Summary of Goals Set for Clients")
        self.assertIn("Client: client", email.body)

    def test_send_weekly_professional_summary_multiple_goals(self):
        professional = Professional.objects.create(user=User.objects.create(username="professional", email="professional@example.com"))
        client = UserProfile.objects.create(user=User.objects.create(username="client"))
        professional.clients.add(client)

        # Create multiple goals
        Goal.objects.create(goaltype="Weight Loss", goalvalue=10, startdate="2025-01-01", enddate="2025-02-01", client=client, professional=professional)
        Goal.objects.create(goaltype="Muscle Gain", goalvalue=5, startdate="2025-01-15", enddate="2025-03-01", client=client, professional=professional)

        # Call the task
        send_weekly_professional_summary()

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("Weight Loss", email.body)
        self.assertIn("Muscle Gain", email.body)

    def test_send_weekly_professional_summary_no_goals(self):
        professional = Professional.objects.create(user=User.objects.create(username="professional", email="professional@example.com"))

        # Call the task
        send_weekly_professional_summary()

        # Check that no email was sent
        self.assertEqual(len(mail.outbox), 0)

class GoalModelTests(TestCase):
    def test_goal_creation(self):
        # Set up test data
        professional = Professional.objects.create(user=User.objects.create(username="professional"))
        client = UserProfile.objects.create(user=User.ob