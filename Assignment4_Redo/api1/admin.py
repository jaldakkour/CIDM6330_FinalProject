
from django.contrib import admin
from .models import SanareSoma

@admin.register(SanareSoma)
class SanareSomaAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    list_filter = ('title',)
    ordering = ('title',)
    list_per_page = 10
    list_editable = ('description',)

    fieldsets = (
        (None, {
            'fields': ('title', 'description')
        }),
    )
    prepopulated_fields = {'description': ('title',)}   

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

