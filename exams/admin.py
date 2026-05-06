from django.contrib import admin
from .models import Exam

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'user', 'exam_date', 'target_score', 'countdown_days')
    list_filter = ('exam_date', 'subject', 'user')
    search_fields = ('name', 'subject__name', 'user__email', 'user__username')
    date_hierarchy = 'exam_date'
