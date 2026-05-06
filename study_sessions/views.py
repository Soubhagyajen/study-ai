from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsOwner
from .models import StudySession
from .serializers import StudySessionSerializer

class StudySessionViewSet(viewsets.ModelViewSet):
    """
    Adhyayan session ViewSet supporting logging/timers.
    """
    serializer_class = StudySessionSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return StudySession.objects.for_user(self.request.user).select_related_models()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Manually end an ongoing Session cleanly hitting the Fat model calculation flow.
        """
        session = self.get_object()
        if session.end_time:
            return Response(
                {"detail": "This session is already closed."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delegates completely to the Fat model
        session.complete_session()
        
        return Response(self.get_serializer(session).data)

    @action(detail=False, methods=['get'], url_path='weekly-stats')
    def weekly_stats(self, request):
        """
        Returns total study hours per day for the last 7 days natively via SQL.
        """
        from django.db.models import Sum
        from django.db.models.functions import TruncDate

        weekly_sessions = self.get_queryset().this_week().annotate(
            date=TruncDate('start_time')
        ).values('date').annotate(
            total_minutes=Sum('duration_minutes')
        ).order_by('date')

        data = [
            {
                "date": entry['date'].strftime('%Y-%m-%d'), 
                "total_minutes": entry['total_minutes'],
                "total_hours": round(entry['total_minutes'] / 60.0, 2)
            }
            for entry in weekly_sessions if entry['date']
        ]
        return Response(data)
