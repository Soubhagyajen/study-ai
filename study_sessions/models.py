from django.db import models
from django.conf import settings
from django.utils import timezone
from subjects.models import Subject, Topic
from datetime import timedelta

class StudySessionQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)

    def select_related_models(self):
        """
        Optimize with select_related for Subject and Topic 
        to avoid N+1 queries.
        """
        return self.select_related('subject', 'topic')

    def today(self):
        """
        'Aaj Ka Adhyayan' logic.
        """
        now = timezone.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        return self.filter(start_time__gte=start_of_day, start_time__lt=end_of_day)

    def this_week(self):
        """
        'Saptah Chart' logic context. Filter sessions in the last 7 days.
        """
        seven_days_ago = timezone.now() - timedelta(days=7)
        return self.filter(start_time__gte=seven_days_ago)

class StudySession(models.Model):
    """
    Adhyayan - Represents a block of time spent studying.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='study_sessions')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='study_sessions')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='study_sessions')
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=0, help_text="Total minutes studied")
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StudySessionQuerySet.as_manager()

    class Meta:
        ordering = ['-start_time']

    def __str__(self):
        return f"Study Session on {self.subject.name} - {self.duration_minutes} mins"

    def complete_session(self, end_time=None):
        """
        Fat model logic for ending a study session and calculating duration.
        """
        if not self.end_time:
            self.end_time = end_time or timezone.now()
            
            # Re-read from db or ensure self.start_time is valid timezone-aware object
            duration = self.end_time - self.start_time
            self.duration_minutes = int(duration.total_seconds() / 60)
            self.save(update_fields=['end_time', 'duration_minutes', 'updated_at'])
            
            # Opportunity: Update Sadhana streak logic here if necessary
            from users.services import update_user_streak
            update_user_streak(self.user)
