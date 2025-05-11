from .models import Professional, UserProfile, Goal

class ProfessionalRepository:
    @staticmethod
    def get_professional_by_user(user):
        return Professional.objects.filter(user=user).first()

    @staticmethod
    def get_clients_for_professional(professional):
        return professional.clients.select_related('user').all()

class UserProfileRepository:
    @staticmethod
    def get_user_profile_by_id(user_id):
        return UserProfile.objects.filter(id=user_id).first()

    @staticmethod
    def get_user_profile_by_user(user):
        return UserProfile.objects.filter(user=user).first()

class GoalRepository:
    @staticmethod
    def create_goal(goaltype, goalvalue, startdate, enddate, client, professional):
        return Goal.objects.create(
            goaltype=goaltype,
            goalvalue=goalvalue,
            startdate=startdate,
            enddate=enddate,
            client=client,
            professional=professional,
        )

