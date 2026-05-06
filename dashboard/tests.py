from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class DashboardAPITests(APITestCase):
    """
    Validates REST Framework payload projection and JWT Authorization configurations.
    """
    def setUp(self):
        self.user = User.objects.create_user(email='shishya@gurukul.ai', username='shishya', password='password123')
        
        # Simulating active JWT configuration flow natively
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'email': 'shishya@gurukul.ai', 'password': 'password123'})
        self.token = response.data['access']
        
        # Lock our test client aggressively into bearer standard
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_dashboard_summary_requires_auth(self):
        """Ensure endpoints strictly enforce standard REST auth."""
        self.client.credentials() # Dropping the JWT purposely
        url = reverse('dashboard-summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_dashboard_summary_success(self):
        """Validating aggregate payload consistency combining multiple databases instances cleanly."""
        url = reverse('dashboard-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Checking composite structures defined internally
        self.assertIn('namaste', response.data)
        self.assertIn('upcoming_exams', response.data)
        self.assertIn('subjects_progress', response.data)
        self.assertIn('today_sessions', response.data)
        self.assertIn('weekly_stats', response.data)

    def test_ai_planner_success(self):
        """Ensures the heuristic logic outputs smart_plan successfully without crashing on empty db contexts."""
        url = reverse('ai-planner')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ai_insight', response.data)
        self.assertIn('smart_plan', response.data)
        self.assertIsInstance(response.data['smart_plan'], list)
