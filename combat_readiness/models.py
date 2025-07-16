from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.db.models.signals import post_migrate, post_save, pre_save, post_delete
from django.dispatch import receiver
import logging
from django.utils import timezone
import threading

# Thread-local storage for current user
_user = threading.local()

def set_current_user(user):
    _user.value = user

def get_current_user():
    return getattr(_user, 'value', None)

# Middleware to set current user for audit logging
class CurrentUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    def __call__(self, request):
        set_current_user(request.user if request.user.is_authenticated else None)
        response = self.get_response(request)
        return response

# Helper to log audit events
def log_audit(instance, action, changes=None):
    from .models import AuditLog
    user = get_current_user()
    AuditLog.objects.create(
        user=user,
        action=action,
        model=instance.__class__.__name__,
        object_id=str(instance.pk),
        object_repr=str(instance),
        changes=changes or ''
    )

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
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# ✅ User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profile_images/', default='default.jpg')
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text='For SMS notifications (optional)')
    receive_email_notifications = models.BooleanField(default=True, help_text='Receive important email notifications')
    receive_sms_notifications = models.BooleanField(default=False, help_text='Receive important SMS notifications')

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def get_image_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        return '/media/profile_images/default.jpg'

    def short_bio(self, length=50):
        if self.bio:
            return self.bio[:length] + ('...' if len(self.bio) > length else '')
        return ''

    def wants_email(self):
        return self.receive_email_notifications

    def wants_sms(self):
        return self.receive_sms_notifications and bool(self.phone_number)

    def clean(self):
        from django.core.exceptions import ValidationError
        # Validate bio length
        if self.bio and len(self.bio) > 500:
            raise ValidationError('Bio cannot exceed 500 characters.')
        # Validate image type and size (if needed)
        if self.profile_image:
            valid_types = ['image/jpeg', 'image/png', 'image/gif']
            if hasattr(self.profile_image.file, 'content_type'):
                if self.profile_image.file.content_type not in valid_types:
                    raise ValidationError('Profile image must be JPEG, PNG, or GIF.')
            # Optionally, check file size (e.g., max 2MB)
            if self.profile_image.size > 2 * 1024 * 1024:
                raise ValidationError('Profile image file size may not exceed 2MB.')
        # Validate phone number if SMS is enabled
        if self.receive_sms_notifications and not self.phone_number:
            raise ValidationError('Phone number required for SMS notifications.')

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

    def get_active_missions(self):
        return self.missions.filter(status='Active')

    def get_assigned_equipment(self):
        return self.equipment_set.all()

    def is_active(self):
        return self.status == 'Active'

    def clean(self):
        from django.core.exceptions import ValidationError
        # Retired soldiers cannot be assigned to active missions
        if self.status == 'Retired' and self.missions.filter(status='Active').exists():
            raise ValidationError('Retired soldiers cannot be assigned to active missions.')

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

    def is_available(self):
        return self.assigned_to is None and self.condition in ["New", "Good"]

    def get_missions(self):
        return self.missions.all()

    def clean(self):
        from django.core.exceptions import ValidationError
        # Equipment needing repair cannot be assigned
        if self.condition == 'Needs Repair' and (self.assigned_to or self.missions.exists()):
            raise ValidationError('Equipment needing repair cannot be assigned to a soldier or mission.')

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

    def is_up_to_date(self):
        import datetime
        return (datetime.date.today() - self.last_training_date).days <= 180

    def get_readiness_color(self):
        return {
            'Excellent': 'green',
            'Good': 'blue',
            'Fair': 'orange',
            'Poor': 'red',
        }.get(self.overall_readiness, 'gray')

    def clean(self):
        from django.core.exceptions import ValidationError
        import datetime
        if not (0 <= self.fitness_score <= 100):
            raise ValidationError('Fitness score must be between 0 and 100.')
        if self.last_training_date > datetime.date.today():
            raise ValidationError('Last training date cannot be in the future.')

# 🚀 Mission/Operation Model
class Mission(models.Model):
    STATUS_CHOICES = [
        ('Planned', 'Planned'),
        ('Active', 'Active'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Normal', 'Normal'),
        ('High', 'High'),
        ('Critical', 'Critical'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Planned')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Normal')
    assigned_soldiers = models.ManyToManyField('Soldier', blank=True, related_name='missions')
    assigned_equipment = models.ManyToManyField('Equipment', blank=True, related_name='missions')
    created_by = models.ForeignKey('CustomUser', on_delete=models.SET_NULL, null=True, related_name='created_missions')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.status})"

    def is_overdue(self):
        import datetime
        if self.end_date and self.status not in ["Completed", "Cancelled"]:
            return self.end_date < datetime.date.today()
        return False

    def num_assigned_soldiers(self):
        return self.assigned_soldiers.count()

    def num_assigned_equipment(self):
        return self.assigned_equipment.count()

    def clean(self):
        from django.core.exceptions import ValidationError
        import datetime
        if self.end_date and self.end_date < self.start_date:
            raise ValidationError('End date cannot be before start date.')
        # Only active soldiers can be assigned
        if self.pk:  # Only check if mission exists (not during initial creation)
            for soldier in self.assigned_soldiers.all():
                if not soldier.is_active():
                    raise ValidationError(f'Soldier {soldier.name} is not active and cannot be assigned to a mission.')

# 🚨 Notification Model
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('success', 'Success'),
        ('danger', 'Danger'),
    ]
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    link = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES, default='info')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"To {self.recipient.username}: {self.message[:30]}..."

    def mark_as_read(self):
        self.is_read = True
        self.save(update_fields=["is_read"])

    def mark_as_unread(self):
        self.is_read = False
        self.save(update_fields=["is_read"])

    def get_type_color(self):
        return {
            'info': 'primary',
            'warning': 'warning',
            'success': 'success',
            'danger': 'danger',
        }.get(self.type, 'secondary')

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.message or not self.message.strip():
            raise ValidationError('Notification message cannot be empty.')
        valid_types = [choice[0] for choice in self.NOTIFICATION_TYPES]
        if self.type not in valid_types:
            raise ValidationError(f'Notification type must be one of: {", ".join(valid_types)}')

# ✅ Create Default Groups Automatically After Migrations
def create_default_groups(sender, **kwargs):
    roles = ['Admin', 'Medical Officer', 'Unit Leader', 'Soldier']
    for role in roles:
        Group.objects.get_or_create(name=role)

post_migrate.connect(create_default_groups, sender=Group)

# Signal to auto-create Soldier when a CustomUser with role 'soldier' is created
@receiver(post_save, sender=CustomUser)
def create_soldier_for_user(sender, instance, created, **kwargs):
    if created and instance.role == 'soldier':
        if not hasattr(instance, 'soldier'):
            Soldier.objects.create(user=instance, name=instance.get_full_name() or instance.username, rank='', unit='', status='Active')

# Signal to notify when equipment condition changes to 'Needs Repair'
@receiver(pre_save, sender=Equipment)
def notify_equipment_needs_repair(sender, instance, **kwargs):
    if not instance.pk:
        return  # New object, no previous state
    try:
        previous = Equipment.objects.get(pk=instance.pk)
    except Equipment.DoesNotExist:
        return
    if previous.condition != 'Needs Repair' and instance.condition == 'Needs Repair':
        # Replace with actual notification logic as needed
        logging.warning(f"Equipment '{instance.name}' now needs repair!")

# Signal to notify when a report is created with 'Poor' readiness
@receiver(post_save, sender=ReadinessReport)
def notify_poor_readiness_report(sender, instance, created, **kwargs):
    if created and instance.overall_readiness == 'Poor':
        logging.warning(f"Readiness report for {instance.soldier.name} is POOR!")

# Signal to notify when a mission is marked as Completed or Cancelled
@receiver(post_save, sender=Mission)
def notify_mission_status_change(sender, instance, **kwargs):
    if instance.status in ["Completed", "Cancelled"]:
        logging.info(f"Mission '{instance.name}' has been marked as {instance.status}.")

# Signal to log when a danger notification is created
@receiver(post_save, sender=Notification)
def notify_danger_notification(sender, instance, created, **kwargs):
    if created and instance.type == 'danger':
        logging.error(f"DANGER notification for {instance.recipient.username}: {instance.message}")

class TrainingEvent(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_training_events')

    def __str__(self):
        return f"{self.name} ({self.date})"

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    model = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    object_repr = models.CharField(max_length=255)
    changes = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} {self.user} {self.action} {self.model} {self.object_repr}"

# Connect signals for major models
for model in [Mission, Soldier, Equipment, ReadinessReport, TrainingEvent, Notification, UserProfile]:
    def make_post_save(model):
        def handler(sender, instance, created, **kwargs):
            action = 'create' if created else 'update'
            log_audit(instance, action)
        return handler
    post_save.connect(make_post_save(model), sender=model)
    def make_post_delete(model):
        def handler(sender, instance, **kwargs):
            log_audit(instance, 'delete')
        return handler
    post_delete.connect(make_post_delete(model), sender=model)
