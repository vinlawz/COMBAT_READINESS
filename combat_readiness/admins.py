from django.contrib import admin
from .models import Soldier, Equipment, ReadinessReport
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


admin.site.register(Soldier)
admin.site.register(Equipment)
admin.site.register(ReadinessReport)
admin.site.register(CustomUser, UserAdmin)