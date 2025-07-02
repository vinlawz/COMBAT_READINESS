from django.core.management.base import BaseCommand
from combat_readiness.models import CustomUser

class Command(BaseCommand):
    help = 'Create a test admin user (username: admin, password: admin123)'

    def handle(self, *args, **kwargs):
        if CustomUser.objects.filter(username='admin').exists():
            self.stdout.write(self.style.WARNING('Admin user already exists.'))
        else:
            user = CustomUser.objects.create_user(username='admin', password='admin123', role='admin', email='admin@example.com')
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(self.style.SUCCESS('Test admin user created: username=admin, password=admin123')) 