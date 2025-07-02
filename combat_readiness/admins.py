from django.contrib import admin
from .models import Soldier, Equipment, ReadinessReport, Mission
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('role',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('role',)}),)

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'priority', 'start_date', 'end_date', 'created_by')
    list_filter = ('status', 'priority', 'start_date', 'end_date')
    search_fields = ('name', 'description', 'location', 'notes')
    filter_horizontal = ('assigned_soldiers', 'assigned_equipment')

admin.site.register(Soldier)
admin.site.register(Equipment)
admin.site.register(ReadinessReport)
admin.site.register(CustomUser, UserAdmin)