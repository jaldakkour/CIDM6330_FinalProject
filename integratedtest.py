import time
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from celery.result import AsyncResult

class CeleryIntegrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_add_numbers_integration(self):
        url = reverse('add-numbers')
        response = self.client.post(url, {'x': 5, 'y': 10}, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        task_id = response.data['task_id']
        result = AsyncResult(task_id)

        # Wait for the task to complete (add a timeout to prevent indefinite blocking)
        timeout = 5  # seconds
        start_time = time.time()
        while not result.ready():
            time.sleep(0.1)
            if time.time() - start_time > timeout:
                self.fail(f"Celery task {task_id} did not complete within the timeout.")

        self.assertTrue(result.successful())
        self.assertEqual(result.get(), 15)
        