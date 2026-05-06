from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsOwner
from .models import Subject, Topic
from .serializers import SubjectSerializer, TopicSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    """
    Vishay CRUD operations.
    Keeps views thin by pushing SQL aggregation heavily inside the QuerySet object.
    """
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Triggers .with_completion_stats() to resolve progress computations safely without N+1
        return Subject.objects.active_for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def progress(self, request):
        """
        Returns condensed payload for progress visualizations.
        Leverages annotated QuerySet.
        """
        subjects = self.get_queryset()
        data = [
            {
                "id": sub.id,
                "name": sub.name,
                "color_code": sub.color_code,
                "total_topics": getattr(sub, 'total_topics', 0),
                "completed_topics": getattr(sub, 'completed_topics', 0),
                "progress_percentage": sub.progress_percentage
            } for sub in subjects
        ]
        return Response(data)

class TopicViewSet(viewsets.ModelViewSet):
    """
    Individual study topics management.
    """
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Access protection relying strictly on the CustomQuerySet nested link
        return Topic.objects.fetch_with_subject().filter(subject__user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        topic = self.get_object()
        confidence = request.data.get('confidence_level')
        
        # Dispatches entirely to Fat Model functionality for pure 'thin view' architecture
        topic.mark_completed(confidence=confidence)
        
        return Response(self.get_serializer(topic).data, status=status.HTTP_200_OK)
