from django.test import TestCase
from .models import CustomUser
from django.urls import reverse
from .models import Soldier
from django.test import RequestFactory
from .views import dashboard_view
from .models import Mission

class CustomUserModelTestCase(TestCase):
    def test_create_custom_user(self):
        user = CustomUser.objects.create_user(username="testuser", password="testpass", role="admin")
        self.assertEqual(user.role, "admin")
        self.assertEqual(str(user), "testuser (Admin)")

class SoldierListViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser2", password="testpass2", role="admin")
        self.soldier = Soldier.objects.create(name="Jane Doe", rank="Captain", unit="Bravo", status="Active")

    def test_soldier_list_view(self):
        self.client.login(username="testuser2", password="testpass2")
        response = self.client.get(reverse("soldier-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Jane Doe")

class SoldierDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser3", password="testpass3", role="admin")
        self.soldier = Soldier.objects.create(name="Alice Smith", rank="Sergeant", unit="Charlie", status="Active")

    def test_soldier_detail_view(self):
        self.client.login(username="testuser3", password="testpass3")
        response = self.client.get(reverse("soldier-detail", args=[self.soldier.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alice Smith")
        self.assertContains(response, "Sergeant")

class DashboardViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser4", password="testpass4", role="admin")
        self.client.login(username="testuser4", password="testpass4")

    def test_dashboard_view(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        # Check for actual content in the dashboard template
        self.assertContains(response, "Welcome,")
        self.assertContains(response, "System Readiness")
        self.assertContains(response, "Soldiers")
        self.assertContains(response, "Equipment")

class MissionListViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser5", password="testpass5", role="admin")
        self.mission = Mission.objects.create(
            name="Operation Dawn",
            description="Early morning operation.",
            status="Planned",
            start_date="2025-07-10",
            priority="High"
        )
        self.client.login(username="testuser5", password="testpass5")

    def test_mission_list_view(self):
        response = self.client.get(reverse("mission-list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Operation Dawn")

class MissionDetailViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser6", password="testpass6", role="admin")
        self.mission = Mission.objects.create(
            name="Operation Sunset",
            description="Evening operation.",
            status="Active",
            start_date="2025-07-11",
            priority="Normal"
        )
        self.client.login(username="testuser6", password="testpass6")

    def test_mission_detail_view(self):
        response = self.client.get(reverse("mission-detail", args=[self.mission.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Operation Sunset")
        self.assertContains(response, "Evening operation.") 

class ProfileEditViewTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="testuser7", 
            password="testpass7", 
            role="admin",
            first_name="Test",
            last_name="User",
            email="test7@example.com"
        )
        # Create a soldier profile for the user
        self.soldier = Soldier.objects.create(
            user=self.user,
            name=f"{self.user.first_name} {self.user.last_name}",
            rank="Private",
            unit="Alpha",
            status="Active"
        )
        self.client.login(username="testuser7", password="testpass7")

    def test_profile_edit_view_get(self):
        response = self.client.get(reverse("profile-edit"))
        self.assertEqual(response.status_code, 200)
        # Check for actual form fields in the template
        self.assertContains(response, "Edit Your Profile")
        self.assertContains(response, "First Name")
        self.assertContains(response, "Last Name")
        self.assertContains(response, "Email")
        self.assertContains(response, "Profile Photo")
        
    def test_profile_edit_view_post(self):
        response = self.client.post(
            reverse("profile-edit"),
            data={
                'first_name': 'Updated',
                'last_name': 'Name',
                'email': 'updated@example.com',
                'phone_number': '+1234567890',
                'bio': 'Test bio',
                'receive_email_notifications': 'on',
                'receive_sms_notifications': 'on'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.last_name, 'Name')
        self.assertEqual(self.user.email, 'updated@example.com')
        self.assertEqual(self.user.profile.phone_number, '+1234567890')
        self.assertEqual(self.user.profile.bio, 'Test bio')
        self.assertTrue(self.user.profile.receive_email_notifications)
        self.assertTrue(self.user.profile.receive_sms_notifications)