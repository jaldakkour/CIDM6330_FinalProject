from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    Professional,
    Goal,
    Activity,
    Routine,
    Food,
    Meal,
    Nutrition,
    Client,
    UserProfile,
    MealFood,
)
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

PTUser = get_user_model()  # Use PTUser instead of User

# Define a new UserAdmin class that inherits from the default UserAdmin
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

# Register your custom UserAdmin
admin.site.unregister(PTUser)  # Unregister the default UserAdmin
admin.site.register(PTUser, CustomUserAdmin)  # Register your custom UserAdmin


# Register your models here.
@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ('PTUser', 'profession', 'specialty')
    search_fields = ('PTUser__username', 'profession', 'specialty')
    raw_id_fields = ('PTUser',)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('goaltype', 'goalvalue', 'startdate', 'enddate', 'client', 'professional')
    raw_id_fields = ('client', 'professional')

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('activitydate', 'starttime', 'endtime', 'activitytype')
    list_filter = ('activitydate', 'activitytype')
    search_fields = ('activitytype',)

@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    filter_horizontal = ('activities',)

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'servingsize', 'servingunit', 'calories')
    search_fields = ('name', 'brand')
    list_filter = ('servingunit',)

class MealFoodInline(admin.TabularInline):
    model = MealFood
    extra = 1

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('mealdate', 'mealtime', 'mealtype')
    list_filter = ('mealdate', 'mealtype')
    inlines = (MealFoodInline,)
    
@admin.register(Nutrition)
class NutritionAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    filter_horizontal = ('meals',)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('PTUser', 'professional')
    raw_id_fields = ('PTUser', 'professional')
    search_fields = ('PTUser__username', 'professional__PTUser__username')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('PTUser', 'gender', 'dateofbirth')
    raw_id_fields = ('PTUser', 'routine', 'nutrition', 'professional')  # Removed 'goal' as it doesn't exist
    search_fields = ('PTUser__username',)
    list_filter = ('gender', 'dateofbirth')
