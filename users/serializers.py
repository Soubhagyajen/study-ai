from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import UserProfile

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'sadhana_streak', 'level', 'experience_points']
        read_only_fields = ['sadhana_streak', 'level', 'experience_points']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_student', 'is_teacher', 'profile']
        read_only_fields = ['id', 'is_student', 'is_teacher']
