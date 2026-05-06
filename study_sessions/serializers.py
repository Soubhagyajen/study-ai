from rest_framework import serializers
from .models import StudySession

class StudySessionSerializer(serializers.ModelSerializer):
    subject_name = serializers.ReadOnlyField(source='subject.name')
    topic_name = serializers.ReadOnlyField(source='topic.name')
    is_completed = serializers.SerializerMethodField()

    def get_is_completed(self, obj):
        return obj.end_time is not None

    class Meta:
        model = StudySession
        fields = [
            'id', 'subject', 'subject_name', 'topic', 'topic_name',
            'start_time', 'end_time', 'duration_minutes', 'notes', 'created_at',
            'is_completed'
        ]
        read_only_fields = ['id', 'duration_minutes', 'created_at', 'is_completed']

    def validate(self, data):
        """
        Entity-level validation for Adhyayan Session constraints.
        - end_time must be after start_time if both exist
        - Topic must belong to the chosen Subject (Vishay)
        """
        start_time = data.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = data.get('end_time', getattr(self.instance, 'end_time', None))

        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError({"end_time": "Study session must end after it starts."})

        subject = data.get('subject', getattr(self.instance, 'subject', None))
        topic = data.get('topic', getattr(self.instance, 'topic', None))
        
        if topic and subject and topic.subject != subject:
            raise serializers.ValidationError({"topic": "This topic does not belong to the selected Vishay."})

        return data
