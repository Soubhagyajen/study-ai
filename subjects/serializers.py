from rest_framework import serializers
from .models import Subject, Topic

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'subject', 'name', 'is_completed', 'confidence_level', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_confidence_level(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Confidence level must be between 0 and 100.")
        return value

class SubjectSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    
    # Annotated fields from CustomQuerySet
    total_topics = serializers.IntegerField(read_only=True, required=False)
    completed_topics = serializers.IntegerField(read_only=True, required=False)
    avg_confidence = serializers.FloatField(read_only=True, required=False)

    class Meta:
        model = Subject
        fields = [
            'id', 'name', 'description', 'color_code', 
            'topics', 'progress_percentage', 'total_topics', 
            'completed_topics', 'avg_confidence', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate_color_code(self, value):
        if not value.startswith('#') or len(value) != 7:
            raise serializers.ValidationError("Color code must be a valid 7-character hex, e.g., #c9963a.")
        return value
