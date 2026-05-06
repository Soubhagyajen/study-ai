from django.contrib import admin
from .models import Subject, Topic

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'progress_percentage_display')
    search_fields = ('name', 'user__email', 'user__username')
    inlines = [TopicInline]
    
    def progress_percentage_display(self, obj):
        return f"{obj.progress_percentage}%"
    progress_percentage_display.short_description = 'Adhyayan Pragati'

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'is_completed', 'confidence_level')
    list_filter = ('is_completed', 'subject')
    search_fields = ('name', 'subject__name')
