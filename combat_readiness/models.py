from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

# User Roles
USER_ROLES = [
    ('admin', 'Admin'),
    ('medical_officer', 'Medical Officer'),
    ('unit_leader', 'Unit Leader'),
    ('soldier', 'Soldier'),
]

# 🚀 Custom User Model
class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=USER_ROLES, default='soldier')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# ✅ User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', default='default.jpg')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# ✅ Auto-create and save profile on user creation/update
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()

# 🚀 Soldier Model
class Soldier(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='soldier')
    name = models.CharField(max_length=100)
    rank = models.CharField(max_length=50)
    unit = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=[
        ('Active', 'Active'),
        ('Reserve', 'Reserve'),
        ('Retired', 'Retired')
    ])

    def __str__(self):
        return self.name

# 🚀 Equipment Model
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    condition = models.CharField(max_length=50, choices=[
        ('New', 'New'),
        ('Good', 'Good'),
        ('Needs Repair', 'Needs Repair')
    ])
    assigned_to = models.ForeignKey(Soldier, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

# 🚀 Readiness Report Model
class ReadinessReport(models.Model):
    soldier = models.ForeignKey(Soldier, on_delete=models.CASCADE)
    fitness_score = models.IntegerField()
    last_training_date = models.DateField()
    overall_readiness = models.CharField(max_length=50, choices=[
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor')
    ])

    def __str__(self):
        return f"{self.soldier.name} - {self.overall_readiness}"

# ✅ Create Default Groups Automatically After Migrations
def create_default_groups(sender, **kwargs):
    roles = ['Admin', 'Medical Officer', 'Unit Leader', 'Soldier']
    for role in roles:
        Group.objects.get_or_create(name=role)

post_migrate.connect(create_default_groups, sender=Group)
