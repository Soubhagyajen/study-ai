from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import GurukulTokenObtainPairView
from users.firebase_auth import FirebaseLoginView

from subjects.views import SubjectViewSet, TopicViewSet
from exams.views import ExamViewSet
from study_sessions.views import StudySessionViewSet
from dashboard.views import DashboardSummaryView, AIPlannerView
from users.views import UserProfileView

# Configure the DRF DefaultRouter for seamless ViewSet mapping
router = DefaultRouter()
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'study-sessions', StudySessionViewSet, basename='studysession')

from django.views.generic import TemplateView

urlpatterns = [
    # 🏠 Frontend HTML Templates (Direct Serving)
    path('', TemplateView.as_view(template_name='gurukul_ashram.html'), name='index'),
    path('gurukul_dashboard.html', TemplateView.as_view(template_name='gurukul_dashboard.html')),
    path('gurukul_vishay.html', TemplateView.as_view(template_name='gurukul_vishay.html')),
    path('gurukul_pariksha.html', TemplateView.as_view(template_name='gurukul_pariksha.html')),
    path('gurukul_planner.html', TemplateView.as_view(template_name='gurukul_planner.html')),
    path('gurukul_ashram.html', TemplateView.as_view(template_name='gurukul_ashram.html')),

    path('admin/', admin.site.urls),
    
    # 🔐 JWT Authentication Endpoints
    path('api/auth/login/', GurukulTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/firebase-login/', FirebaseLoginView.as_view(), name='firebase-login'),
    
    # 🧘 Ashram (Profile/Settings) & Dashboard Endpoints
    path('api/ashram/', UserProfileView.as_view(), name='ashram-profile'),
    path('api/dashboard/', DashboardSummaryView.as_view(), name='dashboard-summary'),
    path('api/ai-planner/', AIPlannerView.as_view(), name='ai-planner-legacy'),
    path('api/ai/generate-plan/', AIPlannerView.as_view(), name='ai-generate-plan'),
    
    # 📡 Main API Router
    path('api/', include(router.urls)),
]

# Debug integrations removed for frontend clarity
