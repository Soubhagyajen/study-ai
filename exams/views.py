from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsOwner
from .models import Exam
from .serializers import ExamSerializer

class ExamViewSet(viewsets.ModelViewSet):
    """
    Pariksha viewsets focusing cleanly on exposing API features.
    """
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Encapsulates logic completely within `get_with_subjects` Manager
        return Exam.objects.get_with_subjects(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
