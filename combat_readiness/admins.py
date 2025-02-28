from django.contrib import admin
from .models import Soldier, Equipment, ReadinessReport
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('role',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('role',)}),)

admin.site.register(Soldier)
admin.site.register(Equipment)
admin.site.register(ReadinessReport)
admin.site.register(CustomUser, UserAdmin)