from django.contrib import admin
from .models import StudySession

@admin.register(StudySession)
class StudySessionAdmin(admin.ModelAdmin):
    list_display = ('subject', 'topic', 'user', 'start_time', 'duration_minutes')
    list_filter = ('subject', 'user', 'start_time')
    search_fields = ('subject__name', 'topic__name', 'user__email', 'user__username')
    date_hierarchy = 'start_time'
