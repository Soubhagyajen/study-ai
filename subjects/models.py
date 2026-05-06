from django.db import models
from django.conf import settings
from django.db.models import Count, Q, Avg

class SubjectQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)

    def with_completion_stats(self):
        """
        Optimized QuerySet combining topics data to prevent N+1 queries.
        Calculates total topics and completed topics for the subject.
        """
        return self.annotate(
            total_topics=Count('topics'),
            completed_topics=Count('topics', filter=Q(topics__is_completed=True)),
            avg_confidence=Avg('topics__confidence_level')
        )

class SubjectManager(models.Manager):
    def get_queryset(self):
        return SubjectQuerySet(self.model, using=self._db)

    def active_for_user(self, user):
        return self.get_queryset().for_user(user).with_completion_stats()

class Subject(models.Model):
    """
    Vishay - Represents a course or subject a Shishya is studying.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    color_code = models.CharField(max_length=7, default="#c9963a", help_text="Hex color code for UI")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SubjectManager()

    class Meta:
        ordering = ['name']
        unique_together = ['user', 'name']

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    @property
    def progress_percentage(self):
        """
        Adhyayan Pragati logic wrapped in Fat Model property.
        Relies on annotated fields to avoid queries if `with_completion_stats` is used.
        """
        if hasattr(self, 'total_topics') and hasattr(self, 'completed_topics'):
            if self.total_topics == 0:
                return 0
            return int((self.completed_topics / self.total_topics) * 100)
        
        # Fallback (may cause N+1 if used in loops without annotations)
        total = self.topics.count()
        if total == 0:
            return 0
        completed = self.topics.filter(is_completed=True).count()
        return int((completed / total) * 100)


class TopicQuerySet(models.QuerySet):
    def fetch_with_subject(self):
        return self.select_related('subject')

    def needs_review(self):
        return self.filter(confidence_level__lt=50, is_completed=False)

class Topic(models.Model):
    """
    Topics under a specific Vishay.
    """
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    confidence_level = models.IntegerField(default=0, help_text="0 to 100")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TopicQuerySet.as_manager()

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.name} - {self.subject.name}"

    def mark_completed(self, confidence=None):
        """
        Fat Model method for business logic.
        """
        self.is_completed = True
        if confidence is not None:
            self.confidence_level = confidence
        self.save(update_fields=['is_completed', 'confidence_level', 'updated_at'])
