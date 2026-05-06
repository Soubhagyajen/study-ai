from django.db import models
from django.conf import settings
from django.utils import timezone
from subjects.models import Subject

class ExamQuerySet(models.QuerySet):
    def for_user(self, user):
        return self.filter(user=user)

    def upcoming(self):
        """
        Filters exams that are in the future and orders them by date.
        """
        return self.filter(exam_date__gte=timezone.now()).order_by('exam_date')

    def past_exams(self):
        return self.filter(exam_date__lt=timezone.now()).order_by('-exam_date')

    def get_with_subjects(self, user):
        return self.for_user(user).select_related('subject')

class Exam(models.Model):
    """
    Pariksha - Represents a Shishya's scheduled evaluation.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='exams')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    name = models.CharField(max_length=200, help_text="e.g., Midterms, Final Exams")
    exam_date = models.DateTimeField()
    target_score = models.IntegerField(default=100, help_text="Target marks or percentage")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ExamQuerySet.as_manager()

    class Meta:
        ordering = ['exam_date']

    def __str__(self):
        return f"{self.name} - {self.subject.name} on {self.exam_date.strftime('%Y-%m-%d')}"

    @property
    def countdown_days(self):
        """
        Business logic for 'Pariksha Countdown'.
        """
        now = timezone.now()
        if self.exam_date > now:
            return (self.exam_date - now).days
        return 0

    @property
    def is_past(self):
        return self.exam_date < timezone.now()
