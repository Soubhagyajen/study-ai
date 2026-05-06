import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')
django.setup()

from django.contrib.auth import get_user_model
from subjects.models import Subject, Topic
from exams.models import Exam
from study_sessions.models import StudySession
from users.models import UserProfile

User = get_user_model()
user = User.objects.filter(username='Arjun').first() or User.objects.filter(email='shishya@gurukul.ai').first()

if not user:
    user = User.objects.create_user(username='Arjun', email='shishya@gurukul.ai', password='password123')

# Sync Profile Streak
if hasattr(user, 'profile'):
    user.profile.sadhana_streak = 14
    user.profile.save()

# Create Real Ancient Gurukul Subjects
s1, _ = Subject.objects.get_or_create(user=user, name='Historical Timeline', defaults={'description': 'Chronicles of ancient empires.', 'color_code': '#e8732a'})
s2, _ = Subject.objects.get_or_create(user=user, name='Vedic Mathematics', defaults={'description': 'Ancient computational algorithms.', 'color_code': '#2d7a4f'})
s3, _ = Subject.objects.get_or_create(user=user, name='Syntax & Grammar', defaults={'description': 'Sanskrit syntax and structural linguistics.', 'color_code': '#c9963a'})

# Create DB Topics
if not Topic.objects.filter(subject=s1).exists():
    Topic.objects.create(subject=s1, name='Module 1: Mauryan Strategies', is_completed=True, confidence_level=85)
    Topic.objects.create(subject=s1, name='Module 2: Vedic Civilizations', is_completed=True, confidence_level=80)
    Topic.objects.create(subject=s2, name='Multiplication by 11', is_completed=True, confidence_level=90)
    Topic.objects.create(subject=s2, name='Digital Roots', is_completed=False, confidence_level=35)
    Topic.objects.create(subject=s3, name='Sandhi Rules', is_completed=False, confidence_level=20)
    Topic.objects.create(subject=s3, name='Vowel Gradation', is_completed=False, confidence_level=15)

# Create Next Exams
if not Exam.objects.filter(user=user).exists():
    Exam.objects.create(user=user, subject=s1, name='UPSC Mock V2', exam_date=timezone.now().date() + timedelta(days=24), target_score=85)
    Exam.objects.create(user=user, subject=s3, name='Syntax Final', exam_date=timezone.now().date() + timedelta(days=6), target_score=95)

# Create 7 Days of Saptah Data automatically generated
if not StudySession.objects.filter(user=user).exists():
    for i in range(7):
        date = timezone.now() - timedelta(days=i)
        # Random duration between 30 mins to 3.5 hours
        dur = random.choice([30, 45, 60, 90, 120, 150, 210])
        StudySession.objects.create(user=user, subject=random.choice([s1, s2, s3]), start_time=date, duration_minutes=dur, is_completed=True)
        # Randomly insert double sessions in a day
        if random.choice([True, False]):
            StudySession.objects.create(user=user, subject=random.choice([s1, s2, s3]), start_time=date - timedelta(hours=5), duration_minutes=60, is_completed=True)

print("Gurukul Virtual AI Database Seeded Successfully!")
