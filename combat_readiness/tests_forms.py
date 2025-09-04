from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from .models import Soldier, Equipment, Mission, ReadinessReport
from .forms import (
    UserCreationForm, UserProfileForm, SoldierForm, 
    EquipmentForm, MissionForm, ReadinessReportForm
)

User = get_user_model()

class UserCreationFormTest(TestCase):
    def test_valid_user_creation(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
            'role': 'soldier'
        }
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.role, 'soldier')
        self.assertTrue(user.check_password('ComplexPass123!'))
    
    def test_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'ComplexPass123!',
            'password2': 'DifferentPass123!',
            'role': 'soldier'
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_weak_password(self):
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': '123',
            'password2': '123',
            'role': 'soldier'
        }
        form = UserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

class UserProfileFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role='soldier'
        )
        
    def test_valid_profile_form(self):
        # Create a test image
        test_image = SimpleUploadedFile(
            name='test.jpg',
            content=b'file_content',
            content_type='image/jpeg'
        )
        
        form_data = {
            'bio': 'Test bio',
            'phone_number': '+1234567890',
            'receive_email_notifications': True,
            'receive_sms_notifications': False
        }
        
        files = {'profile_image': test_image}
        form = UserProfileForm(data=form_data, files=files, instance=self.user.profile)
        self.assertTrue(form.is_valid())
        
        profile = form.save()
        self.assertEqual(profile.bio, 'Test bio')
        self.assertEqual(profile.phone_number, '+1234567890')
        self.assertTrue(profile.receive_email_notifications)
        self.assertFalse(profile.receive_sms_notifications)

class SoldierFormTest(TestCase):
    def test_valid_soldier_form(self):
        form_data = {
            'name': 'John Doe',
            'rank': 'Sergeant',
            'unit': 'Alpha',
            'status': 'Active',
            'date_of_birth': '1990-01-01',
            'blood_type': 'O+',
            'allergies': 'None',
            'emergency_contact': 'Jane Doe (Spouse) 555-1234'
        }
        form = SoldierForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        soldier = form.save()
        self.assertEqual(soldier.name, 'John Doe')
        self.assertEqual(soldier.rank, 'Sergeant')
        self.assertEqual(soldier.unit, 'Alpha')
    
    def test_invalid_soldier_form(self):
        # Missing required field 'name'
        form_data = {
            'rank': 'Sergeant',
            'unit': 'Alpha',
            'status': 'Active'
        }
        form = SoldierForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

class EquipmentFormTest(TestCase):
    def test_valid_equipment_form(self):
        user = User.objects.create_user(
            username='equipuser',
            password='testpass123',
            role='admin'
        )
        soldier = Soldier.objects.create(
            user=user,
            name='Test Soldier',
            rank='Private',
            unit='Alpha'
        )
        
        form_data = {
            'name': 'M4 Carbine',
            'category': 'Firearm',
            'serial_number': 'M4-12345',
            'condition': 'Good',
            'last_maintenance_date': timezone.now().date(),
            'next_maintenance_date': timezone.now().date() + timedelta(days=30),
            'assigned_to': soldier.id,
            'notes': 'Test equipment'
        }
        
        form = EquipmentForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        equipment = form.save()
        self.assertEqual(equipment.name, 'M4 Carbine')
        self.assertEqual(equipment.category, 'Firearm')
        self.assertEqual(equipment.assigned_to, soldier)
    
    def test_equipment_condition_validation(self):
        form_data = {
            'name': 'Test Equipment',
            'category': 'Test',
            'condition': 'Invalid Condition',
            'serial_number': 'TEST-001'
        }
        form = EquipmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('condition', form.errors)

class MissionFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='missionuser',
            password='testpass123',
            role='admin'
        )
        
    def test_valid_mission_form(self):
        form_data = {
            'name': 'Operation Test',
            'description': 'Test mission description',
            'status': 'Planned',
            'priority': 'High',
            'start_date': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
            'end_date': (timezone.now() + timedelta(days=14)).strftime('%Y-%m-%d'),
            'location': 'Test Location',
            'objectives': 'Test objectives',
            'required_equipment': 'Test equipment',
            'notes': 'Test notes'
        }
        
        form = MissionForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        
        mission = form.save()
        self.assertEqual(mission.name, 'Operation Test')
        self.assertEqual(mission.status, 'Planned')
        self.assertEqual(mission.priority, 'High')
        self.assertEqual(mission.created_by, self.user)
    
    def test_mission_date_validation(self):
        # End date before start date
        form_data = {
            'name': 'Invalid Date Mission',
            'description': 'Test',
            'status': 'Planned',
            'start_date': timezone.now().date() + timedelta(days=7),
            'end_date': timezone.now().date()
        }
        form = MissionForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('end_date', form.errors)

class ReadinessReportFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='readinessuser',
            password='testpass123',
            role='soldier'
        )
        self.soldier = Soldier.objects.create(
            user=self.user,
            name='Test Soldier',
            rank='Private',
            unit='Alpha'
        )
        
    def test_valid_readiness_report(self):
        form_data = {
            'soldier': self.soldier.id,
            'fitness_score': 85,
            'last_training_date': timezone.now().date(),
            'overall_readiness': 'Good',
            'medical_notes': 'No issues',
            'equipment_condition': 'Good',
            'morale_level': 'High',
            'concerns': 'None',
            'recommendations': 'Continue current training'
        }
        
        form = ReadinessReportForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        report = form.save()
        self.assertEqual(report.soldier, self.soldier)
        self.assertEqual(report.fitness_score, 85)
        self.assertEqual(report.overall_readiness, 'Good')
    
    def test_fitness_score_validation(self):
        # Score out of range
        form_data = {
            'soldier': self.soldier.id,
            'fitness_score': 150,  # Should be 0-100
            'last_training_date': timezone.now().date(),
            'overall_readiness': 'Good'
        }
        form = ReadinessReportForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('fitness_score', form.errors)
