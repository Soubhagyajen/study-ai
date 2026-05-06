from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Custom user model for Gurukul AI replacing the default Django user.
    """
    email = models.EmailField(_('email address'), unique=True)
    is_student = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Custom fields for Gurukul AI
    sadhana_streak = models.IntegerField(default=0, help_text="Number of consecutive study days")
    level = models.IntegerField(default=1, help_text="Shishya level based on XP")
    experience_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.email} Profile"
