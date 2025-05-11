from django.contrib import admin

# Register your models here.
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

User = get_user_model()

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
admin.site.unregister(User)  # Unregister the default UserAdmin
admin.site.register(User, CustomUserAdmin)  # Register your custom UserAdmin


# Register your models here.
@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ('user', 'profession', 'specialty')
    search_fields = ('user__username', 'profession', 'specialty')
    raw_id_fields = ('user',)

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('user', 'goaltype', 'startdate', 'enddate')
    list_filter = ('goaltype', 'startdate', 'enddate')
    search_fields = ('user__username', 'goaltype')
    raw_id_fields = ('user',)

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
    list_display = ('user', 'professional')
    raw_id_fields = ('user', 'professional')
    search_fields = ('user__username', 'professional__user__username')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'dateofbirth')
    raw_id_fields = ('user', 'goal', 'routine', 'nutrition', 'professional') #makes foreign keys selectable.
    search_fields = ('user__username',)
    list_filter = ('gender', 'dateofbirth')

