from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Subject, Topic

User = get_user_model()

class SubjectModelTests(TestCase):
    """
    Core TestCase verifying Fat Model properties and custom managers.
    """
    def setUp(self):
        self.user = User.objects.create_user(email='shishya@gurukul.ai', username='shishya', password='password123')
        self.subject = Subject.objects.create(user=self.user, name='Vedic Mathematics')
        self.topic1 = Topic.objects.create(subject=self.subject, name='Base Arithmetic', is_completed=True, confidence_level=80)
        self.topic2 = Topic.objects.create(subject=self.subject, name='Digital Roots', is_completed=False, confidence_level=30)

    def test_with_completion_stats_manager(self):
        """
        Ensures the complex QuerySet aggregations prevent N+1 natively and calculate accurately.
        """
        subject_stats = Subject.objects.active_for_user(self.user).first()
        self.assertEqual(subject_stats.total_topics, 2)
        self.assertEqual(subject_stats.completed_topics, 1)
        self.assertEqual(subject_stats.avg_confidence, 55.0)
        self.assertEqual(subject_stats.progress_percentage, 50)

    def test_topic_mark_completed(self):
        """
        Validates business logic encapsulation inside the Fat Model.
        """
        self.topic2.mark_completed(confidence=90)
        self.topic2.refresh_from_db()
        self.assertTrue(self.topic2.is_completed)
        self.assertEqual(self.topic2.confidence_level, 90)
