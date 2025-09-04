from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.utils import timezone
from datetime import timedelta
from .models import Soldier, Equipment, Mission, ReadinessReport, Notification
from .views import dashboard_view
import os
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class BaseTest(TestCase):
    def create_user(self, role='soldier', **kwargs):
        """Helper method to create a unique user"""
        username = f'testuser_{self._testMethodName}_{role}'
        email = f'{username}@example.com'
        return User.objects.create_user(
            username=username,
            email=email,
            password='testpass123',
            role=role,
            **kwargs
        )

    def create_soldier(self, user=None, **kwargs):
        """Helper method to create a unique soldier"""
        if not user:
            user = self.create_user()
        return Soldier.objects.create(
            user=user,
            name=f'Test {user.username}',
            rank='Private',
            unit='Alpha',
            status='Active',
            **kwargs
        )

    def tearDown(self):
        """Clean up after tests"""
        User.objects.all().delete()
        Soldier.objects.all().delete()
        Mission.objects.all().delete()
        ReadinessReport.objects.all().delete()
        Notification.objects.all().delete()

class DashboardViewTest(BaseTest):
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.user = self.create_user(role='admin')
        self.client.login(username=self.user.username, password='testpass123')
        
        self.soldier = self.create_soldier()
        self.equipment = Equipment.objects.create(
            name='Test Equipment',
            category='Test',
            condition='Good'
        )
        self.mission = Mission.objects.create(
            name='Test Mission',
            status='Planned',
            start_date=timezone.now().date(),
            created_by=self.user
        )
    
    def test_dashboard_view_authenticated(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')
        self.assertIn('num_soldiers', response.context)
        self.assertIn('num_equipment', response.context)
        self.assertIn('num_missions', response.context)
        self.assertIn('recent_missions', response.context)
        self.assertIn('recent_reports', response.context)
        self.assertIn('recent_notifications', response.context)
    
    def test_dashboard_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")

class SoldierViewTests(BaseTest):
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.user = self.create_user(role='admin')
        self.client.login(username=self.user.username, password='testpass123')
        
        self.soldier = self.create_soldier()
    
    def test_soldier_list_view(self):
        response = self.client.get(reverse('soldier-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'soldiers/list.html')
        self.assertEqual(len(response.context['soldiers']), 1)
    
    def test_soldier_create_view(self):
        response = self.client.post(reverse('soldier-create'), {
            'name': 'New Soldier',
            'rank': 'Sergeant',
            'unit': 'Bravo',
            'status': 'Active'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after creation
        self.assertEqual(Soldier.objects.count(), 2)
        self.assertTrue(Soldier.objects.filter(name='New Soldier').exists())
    
    def test_soldier_update_view(self):
        url = reverse('soldier-update', args=[self.soldier.id])
        response = self.client.post(url, {
            'name': 'Updated Soldier',
            'rank': 'Corporal',
            'unit': 'Charlie',
            'status': 'Active'
        })
        self.assertEqual(response.status_code, 302)
        self.soldier.refresh_from_db()
        self.assertEqual(self.soldier.name, 'Updated Soldier')
        self.assertEqual(self.soldier.rank, 'Corporal')
    
    def test_soldier_delete_view(self):
        url = reverse('soldier-delete', args=[self.soldier.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Soldier.objects.count(), 0)

class MissionViewTests(BaseTest):
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.user = self.create_user(role='admin')
        self.client.login(username=self.user.username, password='testpass123')
        
        self.mission = Mission.objects.create(
            name='Test Mission',
            status='Planned',
            start_date=timezone.now().date(),
            created_by=self.user
        )
    
    def test_mission_list_view(self):
        response = self.client.get(reverse('mission-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'missions/list.html')
        self.assertEqual(len(response.context['missions']), 1)
    
    def test_mission_create_view(self):
        response = self.client.post(reverse('mission-create'), {
            'name': 'New Mission',
            'description': 'Test description',
            'status': 'Planned',
            'start_date': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'priority': 'High'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Mission.objects.count(), 2)
        self.assertTrue(Mission.objects.filter(name='New Mission').exists())
    
    def test_mission_detail_view(self):
        url = reverse('mission-detail', args=[self.mission.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'missions/detail.html')
        self.assertEqual(response.context['mission'], self.mission)

class ReadinessReportViewTests(BaseTest):
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.user = self.create_user(role='soldier')
        self.client.login(username=self.user.username, password='testpass123')
        
        self.soldier = self.create_soldier(user=self.user)
        self.report = ReadinessReport.objects.create(
            soldier=self.soldier,
            fitness_score=85,
            last_training_date=timezone.now().date(),
            overall_readiness='Good'
        )
    
    def test_readiness_report_create(self):
        response = self.client.post(reverse('readiness-create'), {
            'soldier': self.soldier.id,
            'fitness_score': 90,
            'last_training_date': timezone.now().date().strftime('%Y-%m-%d'),
            'overall_readiness': 'Excellent'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ReadinessReport.objects.count(), 2)
    
    def test_readiness_report_update(self):
        url = reverse('readiness-update', args=[self.report.id])
        response = self.client.post(url, {
            'soldier': self.soldier.id,
            'fitness_score': 80,
            'last_training_date': timezone.now().date().strftime('%Y-%m-%d'),
            'overall_readiness': 'Good'
        })
        self.assertEqual(response.status_code, 302)
        self.report.refresh_from_db()
        self.assertEqual(self.report.fitness_score, 80)

class NotificationViewTests(BaseTest):
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.user = self.create_user(role='soldier')
        self.client.login(username=self.user.username, password='testpass123')
        
        self.notification = Notification.objects.create(
            recipient=self.user,
            message='Test notification',
            type='info'
        )
    
    def test_notification_mark_as_read(self):
        self.assertFalse(self.notification.is_read)
        response = self.client.post(reverse('notification-mark-read', args=[self.notification.id]))
        self.assertEqual(response.status_code, 200)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
    
    def test_notification_list_view(self):
        response = self.client.get(reverse('notification-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'notifications/list.html')
        self.assertEqual(len(response.context['notifications']), 1)

class PermissionTests(BaseTest):
    def setUp(self):
        """Set up test data and client"""
        self.client = Client()
        self.user = self.create_user(role='soldier')
        self.client.login(username=self.user.username, password='testpass123')
    
    def test_admin_required_mixin(self):
        # Create a regular user
        user = self.create_user(role='soldier')
        self.client.login(username=user.username, password='testpass123')
        
        # Try to access admin-only view
        response = self.client.get(reverse('admin-dashboard'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Create admin user
        admin = self.create_user(role='admin')
        self.client.login(username=admin.username, password='testpass123')
        
        # Admin should be able to access the view
        response = self.client.get(reverse('admin-dashboard'))
        self.assertEqual(response.status_code, 200)
