from django.contrib import admin
from .models import Soldier, Equipment  # Import models

# Register the models
admin.site.register(Soldier)
admin.site.register(Equipment)
