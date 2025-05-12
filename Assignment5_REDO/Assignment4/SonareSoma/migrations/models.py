from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

PTUser = get_user_model()  # Use Django's built-in User model

class Professional(models.Model):
    """
    Extends the built-in User model to represent a professional.
    """
    PTUser = models.OneToOneField(PTUser, on_delete=models.CASCADE, related_name='professional_profile')
    profession = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Profession'))
    specialty = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Specialty'))

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('Professional')
        verbose_name_plural = _('Professionals')


class Goal(models.Model):
    """
    Represents a user's fitness goal.
    """
    goaltype = models.CharField(max_length=255)  # Example: "Weight Loss", "Muscle Gain"
    goalvalue = models.FloatField()  # Example: Target weight, calories, etc.
    startdate = models.DateField()
    enddate = models.DateField()
    client = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name="goals")
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name="assigned_goals")

    def __str__(self):
        return f"{self.goaltype} for {self.client.user.username} by {self.professional.user.username}"

    class Meta:
        verbose_name = _('Goal')
        verbose_name_plural = _('Goals')


class Activity(models.Model):
    """
    Represents a single activity event.
    """
    activitydate = models.DateField(verbose_name=_('Activity Date'))
    starttime = models.TimeField(verbose_name=_('Start Time'))
    endtime = models.TimeField(verbose_name=_('End Time'))
    activitytype = models.CharField(max_length=255, verbose_name=_('Activity Type'))

    def __str__(self):
        return f"Activity {self.id} - {self.activitytype} on {self.activitydate}"

    class Meta:
        verbose_name = _('Activity')
        verbose_name_plural = _('Activities')


class Routine(models.Model):
    """
    Represents an exercise routine.
    """
    activities = models.ManyToManyField(Activity, related_name='routines', verbose_name=_('Activities'))

    def __str__(self):
        return f"Routine {self.id}"

    class Meta:
        verbose_name = _('Routine')
        verbose_name_plural = _('Routines')


class Food(models.Model):
    """
    Represents a type of food.
    """
    name = models.CharField(max_length=255, verbose_name=_('Food Name'))
    brand = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Brand'))
    servingsize = models.FloatField(verbose_name=_('Serving Size'))
    servingunit = models.CharField(max_length=255, verbose_name=_('Serving Unit'))
    calories = models.FloatField(verbose_name=_('Calories'))
    protein = models.FloatField(verbose_name=_('Protein'))
    carbohydrates = models.FloatField(verbose_name=_('Carbohydrates'))
    fat = models.FloatField(verbose_name=_('Fat'))
    sodium = models.FloatField(verbose_name=_('Sodium'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Food')
        verbose_name_plural = _('Foods')


MEAL_TYPES = [
    ('breakfast', _('Breakfast')),
    ('lunch', _('Lunch')),
    ('dinner', _('Dinner')),
    ('snack', _('Snack')),
]

class Meal(models.Model):
    """
    Represents a meal consumed.
    """
    mealdate = models.DateField(verbose_name=_('Meal Date'))
    mealtime = models.TimeField(verbose_name=_('Meal Time'))
    mealtype = models.CharField(max_length=255, choices=MEAL_TYPES, verbose_name=_('Meal Type'))
    foods = models.ManyToManyField(Food, through='MealFood', related_name='meals', verbose_name=_('Foods'))

    def __str__(self):
        return f"Meal {self.id} on {self.mealdate} at {self.mealtime}"

    class Meta:
        verbose_name = _('Meal')
        verbose_name_plural = _('Meals')


class MealFood(models.Model):
    """
    Through model connecting Meal and Food with quantity.
    """
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, verbose_name=_('Meal'))
    food = models.ForeignKey(Food, on_delete=models.CASCADE, verbose_name=_('Food'))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_('Quantity'))

    def __str__(self):
        return f"{self.quantity} x {self.food.name} in Meal {self.meal.id}"

    class Meta:
        verbose_name = _('Meal Food Item')
        verbose_name_plural = _('Meal Food Items')
        unique_together = ('meal', 'food')  # Prevent duplicate food items in a meal


class Nutrition(models.Model):
    """
    Represents nutritional information or plans. A high-level grouping model.
    """
    meals = models.ManyToManyField(Meal, related_name='nutrition_plans', verbose_name=_('Meals'))

    def __str__(self):
        return f"Nutrition Plan {self.id}"

    class Meta:
        verbose_name = _('Nutrition Plan')
        verbose_name_plural = _('Nutrition Plans')


class Client(models.Model):
    """
    Represents a client relationship with a professional.
    """
    user = models.OneToOneField(PTUser, on_delete=models.CASCADE, related_name='client_profile', verbose_name=_('User'))
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='clients', verbose_name=_('Professional'))

    def __str__(self):
        return f"Client {self.user.username} of {self.professional.user.username}"

    class Meta:
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')


# User Profile (Extending the built-in User)
class UserProfile(models.Model):
    """
    Extends the built-in User model with additional fields.
    """
    user = models.OneToOneField(PTUser, on_delete=models.CASCADE, related_name='user_profile')
    gender = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('Gender'))
    height = models.FloatField(blank=True, null=True, verbose_name=_('Height'))
    weight = models.FloatField(blank=True, null=True, verbose_name=_('Weight'))
    dateofbirth = models.DateField(blank=True, null=True, verbose_name=_('Date of Birth'))
    routine = models.ForeignKey(Routine, on_delete=models.SET_NULL, blank=True, null=True, related_name='user_profiles', verbose_name=_('Routine'))
    nutrition = models.ForeignKey(Nutrition, on_delete=models.SET_NULL, blank=True, null=True, related_name='user_profiles', verbose_name=_('Nutrition'))
    professional = models.ForeignKey(Professional, on_delete=models.SET_NULL, blank=True, null=True, related_name='managed_profiles', verbose_name=_('Professional'))  # Changed related name

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')




