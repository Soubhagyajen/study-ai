from rest_framework import serializers
from django.utils import timezone
from .models import Exam

class ExamSerializer(serializers.ModelSerializer):
    countdown_days = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()
    subject_name = serializers.ReadOnlyField(source='subject.name')

    class Meta:
        model = Exam
        fields = [
            'id', 'subject', 'subject_name', 'name', 'exam_date', 
            'target_score', 'countdown_days', 'is_past', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_exam_date(self, value):
        """Ensure new Pariksha are not scheduled in the past."""
        if self.instance is None and value < timezone.now():
            raise serializers.ValidationError("Pariksha cannot be scheduled in the past.")
        return value

    def validate_target_score(self, value):
        if value < 0:
            raise serializers.ValidationError("Target score cannot be negative.")
        return value
