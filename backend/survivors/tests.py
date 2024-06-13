from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Survivor, Inventory

class SurvivorAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_survivor(self):
        url = reverse('register-survivor')
        data = {
            'name': 'Test Survivor',
            'age': 30,
            'sex': 'male',
            'last_location': {'latitude': 10.1234, 'longitude': -20.5678},
            'inventory': {'water': 5, 'food': 3, 'medication': 2, 'ammunition': 10}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survivor.objects.count(), 1)
        self.assertEqual(Inventory.objects.count(), 1)

    def test_update_location(self):
        survivor = Survivor.objects.create(name='Test Survivor', age=30, sex='M', last_location={'latitude': 0, 'longitude': 0})
        url = reverse('update-location', args=[survivor.name])
        data = {'last_location': {'latitude': 15.6789, 'longitude': -30.9876}}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        survivor.refresh_from_db()
        self.assertEqual(survivor.last_location['latitude'], 15.6789)
        self.assertEqual(survivor.last_location['longitude'], -30.9876)

    def test_report_infection(self):
        reporter = Survivor.objects.create(name='Reporter Survivor', age=25, sex='F', last_location={'latitude': 0, 'longitude': 0})
        survivor = Survivor.objects.create(name='Test Survivor', age=30, sex='M', last_location={'latitude': 0, 'longitude': 0})
        url = reverse('report-infection')
        data = {'reporter_name': reporter.name, 'reported_survivor_name': survivor.name}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        survivor.refresh_from_db()
        self.assertTrue(survivor.infected)

    def test_trade_items(self):
        survivor1 = Survivor.objects.create(name='Survivor 1', age=28, sex='M', last_location={'latitude': 0, 'longitude': 0})
        survivor2 = Survivor.objects.create(name='Survivor 2', age=35, sex='F', last_location={'latitude': 0, 'longitude': 0})
        Inventory.objects.create(survivor=survivor1, water=3, food=2, medication=1, ammunition=5)
        Inventory.objects.create(survivor=survivor2, water=2, food=1, medication=3, ammunition=10)

        url = reverse('trade', args=[survivor1.name])
        data = {
            'other_inventory': survivor2.name,
            'offered_items': {'water': 1, 'food': 1},
            'requested_items': {'ammunition': 6}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        survivor1.refresh_from_db()
        survivor2.refresh_from_db()
        self.assertEqual(survivor1.inventory.ammunition, 6)
        self.assertEqual(survivor2.inventory.water, 4)

    def test_reports(self):
        survivor1 = Survivor.objects.create(name='Survivor 1', age=28, sex='M', last_location={'latitude': 0, 'longitude': 0})
        survivor2 = Survivor.objects.create(name='Survivor 2', age=35, sex='F', last_location={'latitude': 0, 'longitude': 0})
        Inventory.objects.create(survivor=survivor1, water=3, food=2, medication=1, ammunition=5)
        Inventory.objects.create(survivor=survivor2, water=2, food=1, medication=3, ammunition=10)

        url = reverse('reports')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['infected_percentage'], 0.0)  
        self.assertEqual(response.data['avg_water'], 2.5) 


