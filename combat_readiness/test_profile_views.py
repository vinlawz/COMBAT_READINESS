import os
import tempfile
from pathlib import Path
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from .models import UserProfile, Soldier

User = get_user_model()

class ProfilePhotoUploadTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up data for the whole TestCase"""
        # Create a test user that will be used by all test methods
        cls.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='soldier'
        )
        # Create a soldier profile for the user
        cls.soldier = Soldier.objects.create(
            user=cls.user,
            name='Test User',
            rank='Private',
            unit='Alpha',
            status='Active'
        )

    def setUp(self):
        """Set up for each test method"""
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
        
        # Create a small test image
        self.test_image = SimpleUploadedFile(
            name=f'test_image_{self._testMethodName}.jpg',
            content=open(os.path.join(os.path.dirname(__file__), 'static', 'img', 'default-avatar.png'), 'rb').read(),
            content_type='image/jpeg'
        )
    
    def tearDown(self):
        """Clean up after each test method"""
        # Clean up any created files
        try:
            profile = UserProfile.objects.get(user=self.user)
            if profile.profile_image and 'test_image' in str(profile.profile_image):
                if os.path.isfile(profile.profile_image.path):
                    os.remove(profile.profile_image.path)
        except UserProfile.DoesNotExist:
            pass

    def test_upload_profile_photo(self):
        """Test uploading a profile photo"""
        # Get the profile edit page
        response = self.client.get(reverse('profile-edit'))
        self.assertEqual(response.status_code, 200)
        
        # Prepare form data with a test image
        with open(os.path.join(os.path.dirname(__file__), 'static', 'img', 'default-avatar.png'), 'rb') as img:
            response = self.client.post(
                reverse('profile-edit'),
                data={
                    'first_name': 'Test',
                    'last_name': 'User',
                    'email': 'test@example.com',
                    'profile_image': img
                },
                follow=True
            )
        
        # Check if the upload was successful
        self.assertEqual(response.status_code, 200)
        profile = UserProfile.objects.get(user=self.user)
        self.assertIsNotNone(profile.profile_image)
        self.assertTrue(profile.profile_image.url.endswith('.jpg') or profile.profile_image.url.endswith('.png'))
    
    def test_remove_profile_photo(self):
        """Test removing a profile photo"""
        # First, upload a photo
        profile = UserProfile.objects.get(user=self.user)
        profile.profile_image = self.test_image
        profile.save()
        
        # Verify the test image was set
        self.assertIn('test_image', str(profile.profile_image))
        
        # Get the form to include CSRF token
        response = self.client.get(reverse('profile-edit'))
        self.assertEqual(response.status_code, 200)
        csrf_token = response.context['csrf_token']
        
        # Remove the photo by using the clear checkbox
        response = self.client.post(
            reverse('profile-edit'),
            data={
                'csrfmiddlewaretoken': csrf_token,
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@example.com',
                'profile_image-clear': 'on'  # This is how Django handles clearing files
            },
            follow=True
        )
        
        # Check if the photo was removed
        self.assertEqual(response.status_code, 200)
        profile.refresh_from_db()
        self.assertTrue(profile.profile_image)  # Default image should be set
        
        # Check if the current image is not the test image
        self.assertNotIn('test_image', str(profile.profile_image))
        
        # Verify the file was actually removed from the filesystem
        if os.path.exists(profile.profile_image.path) and 'test_image' in profile.profile_image.path:
            self.fail("Test image file was not properly removed")
    
    def test_invalid_file_upload(self):
        """Test uploading an invalid file type"""
        # Create a test text file (not an image)
        invalid_file = SimpleUploadedFile(
            name='test.txt',
            content=b'This is not an image',
            content_type='text/plain'
        )
        
        # Try to upload the invalid file
        response = self.client.post(
            reverse('profile-edit'),
            data={
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@example.com',
                'profile_image': invalid_file
            },
            follow=True
        )
        
        # Check that the file was rejected
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Profile image must be JPEG, PNG, or GIF.')
        
        # Check that no file was saved
        profile = UserProfile.objects.get(user=self.user)
        if profile.profile_image:
            self.assertNotIn('test.txt', str(profile.profile_image))
