from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_student', 'is_teacher', 'is_staff']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Role Information', {'fields': ('is_student', 'is_teacher')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Information', {'fields': ('is_student', 'is_teacher')}),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'sadhana_streak', 'level']
    search_fields = ['user__email', 'user__username']

admin.site.register(CustomUser, CustomUserAdmin)
