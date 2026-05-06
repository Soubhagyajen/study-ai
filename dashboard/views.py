from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.db.models.functions import TruncDate

from subjects.models import Subject
from exams.models import Exam
from study_sessions.models import StudySession
from subjects.serializers import SubjectSerializer
from exams.serializers import ExamSerializer
from study_sessions.serializers import StudySessionSerializer

class DashboardSummaryView(APIView):
    """
    Gurukul Aggregate Hub tailored for Dashboard UI.
    Utilizes optimized ORM queries (TruncDate, Select Related, Annotations)
    to prevent multiple unoptimized SELECT operations.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # 1. Pariksha Countdown (Upcoming exams, limited to top 3)
        upcoming_exams = Exam.objects.for_user(user).upcoming().select_related('subject')[:3]
        
        # 2. Adhyayan Pragati (Subject Progress securely fetching annotated data)
        # Avoids N+1 using .with_completion_stats() natively
        subjects = Subject.objects.active_for_user(user).prefetch_related('topics')[:5]
        
        # 3. Aaj Ka Adhyayan (Today's Study sessions using DB isolation semantics)
        today_sessions = StudySession.objects.for_user(user).today().select_related('subject', 'topic')

        # Calculate today's total focus hours seamlessly
        total_focus_minutes_today = sum(sess.duration_minutes for sess in today_sessions if sess.is_completed) if hasattr(StudySession, 'is_completed') else sum(sess.duration_minutes for sess in today_sessions if sess.end_time)
        total_study_hours_today = round(total_focus_minutes_today / 60.0, 1)

        # 4. Saptah Chart (Weekly Stats Aggregation)
        # Group study session duration by distinct dates within the last 7 days natively in SQL
        weekly_sessions = StudySession.objects.for_user(user).this_week().annotate(
            date=TruncDate('start_time')
        ).values('date').annotate(
            total_minutes=Sum('duration_minutes')
        ).order_by('date')

        saptah_chart_data = [
            {"date": entry['date'].strftime('%Y-%m-%d'), "minutes": entry['total_minutes']}
            for entry in weekly_sessions if entry['date']
        ]
        
        # Profile Data handling
        sadhana_streak = getattr(user, 'profile', None)
        sadhana_streak_value = sadhana_streak.sadhana_streak if sadhana_streak else 0

        # Return comprehensive combined payload 
        return Response({
            'namaste': f"Namaste, {user.username or user.email}",
            'sadhana_streak': sadhana_streak_value,
            'total_study_hours_today': total_study_hours_today,
            'upcoming_exams': ExamSerializer(upcoming_exams, many=True).data,
            'subjects_progress': SubjectSerializer(subjects, many=True).data,
            'today_sessions': StudySessionSerializer(today_sessions, many=True).data,
            'weekly_stats': saptah_chart_data,
        })

from .gemini_service import generate_study_plan

class AIPlannerView(APIView):
    """
    Serves the smart daily plan generator by interfacing natively with Google Gemini JSON API.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        from subjects.models import Subject
        from exams.models import Exam

        subjects = list(Subject.objects.active_for_user(user).values_list('name', flat=True))
        upcoming_exams = list(Exam.objects.for_user(user).upcoming().values('name', 'exam_date'))
        
        # Calculate dynamic streak
        streak = getattr(user, 'profile', None)
        streak_val = streak.sadhana_streak if streak else 0

        user_data = {
            "subjects": subjects,
            "upcoming_exams": str(upcoming_exams),
            "progress": f"Active study streak: {streak_val} days"
        }

        # Invoke Gemini natively
        plan_data = generate_study_plan(user_data)
        
        return Response(plan_data)
