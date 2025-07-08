from django.test import TestCase
from .models import Soldier
from django.urls import reverse

# Create your tests here.

class SimpleTestCase(TestCase):
    def test_basic_addition(self):
        self.assertEqual(1 + 1, 2)

class SoldierModelTestCase(TestCase):
    def test_create_soldier(self):
        soldier = Soldier.objects.create(
            name="Vincent Elias",
            rank="Private",
            unit="Alpha",
            status="Active"
        )
        self.assertEqual(str(soldier), "Private Vincent Elias")
        self.assertEqual(soldier.unit, "Alpha")

class IndexViewTestCase(TestCase):
    def test_index_view_returns_200(self):
        response = self.client.get(reverse('readiness:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Combat Readiness System Home")
