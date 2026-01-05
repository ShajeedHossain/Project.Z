from datetime import datetime

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import AccessLog

# Create your tests here.

class AccessLogAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.access_log_data = {
            'card_id': 'C1001',
            'door_name': 'Main Entrance',
            'access_granted': True
        }
        self.access_log = AccessLog.objects.create(**self.access_log_data)

    def test_create_access_log(self):
        """Test creating a new access log"""
        response = self.client.post(
            '/api/logs/',
            {
                'card_id': 'C1002',
                'door_name': 'Back Door',
                'access_granted': False
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AccessLog.objects.count(), 2)
        self.assertEqual(response.data['card_id'], 'C1002')

    def test_get_all_access_logs(self):
        """Test retrieving all access logs"""
        response = self.client.get('/api/logs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_access_log(self):
        """Test retrieving a single access log"""
        response = self.client.get(f'/api/logs/{self.access_log.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['card_id'], 'C1001')

    def test_update_access_log(self):
        """Test updating an access log"""
        response = self.client.put(
            f'/api/logs/{self.access_log.id}/',
            {
                'card_id': 'C1001',
                'door_name': 'Side Entrance',
                'access_granted': True
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_log.refresh_from_db()
        self.assertEqual(self.access_log.door_name, 'Side Entrance')

    def test_delete_access_log(self):
        """Test deleting an access log"""
        response = self.client.delete(f'/api/logs/{self.access_log.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AccessLog.objects.count(), 0)

    def test_filter_by_card_id(self):
        """Test filtering access logs by card_id"""
        AccessLog.objects.create(
            card_id='C1003',
            door_name='Garage',
            access_granted=True
        )
        response = self.client.get('/api/logs/?card_id=C1001')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['card_id'], 'C1001')
