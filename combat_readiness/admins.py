from django.contrib import admin
from .models import Soldier, Equipment, ReadinessReport, Mission, Notification, UserProfile
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Inline for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('role', 'is_verified')}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('role', 'is_verified')}),)
    inlines = [UserProfileInline]

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'priority', 'start_date', 'end_date', 'created_by')
    list_filter = ('status', 'priority', 'start_date', 'end_date')
    search_fields = ('name', 'description', 'location', 'notes')
    filter_horizontal = ('assigned_soldiers', 'assigned_equipment')

@admin.register(Soldier)
class SoldierAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'unit', 'status', 'user')
    list_filter = ('status', 'unit', 'rank')
    search_fields = ('name', 'rank', 'unit')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'condition', 'assigned_to')
    list_filter = ('condition', 'category')
    search_fields = ('name', 'category')

@admin.register(ReadinessReport)
class ReadinessReportAdmin(admin.ModelAdmin):
    list_display = ('soldier', 'fitness_score', 'last_training_date', 'overall_readiness')
    list_filter = ('overall_readiness', 'last_training_date')
    search_fields = ('soldier__name',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'message', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read', 'created_at')
    search_fields = ('recipient__username', 'message')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_image')
    search_fields = ('user__username', 'bio')

admin.site.register(CustomUser, CustomUserAdmin)