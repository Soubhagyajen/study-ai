from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate

def calculate_sadhana_streak(user):
    """
    Calculates consecutive days the user has studied (Adhyayan sessions).
    Walking backwards from today in the database.
    """
    from study_sessions.models import StudySession
    
    # Get distinct dates of study, descending
    sessions = StudySession.objects.filter(
        user=user, 
        end_time__isnull=False
    ).annotate(
        date=TruncDate('start_time')
    ).values_list('date', flat=True).distinct().order_by('-date')

    if not sessions:
        return 0

    dates = list(sessions)
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    
    streak = 0
    current_date = dates[0]

    # If the most recent session is older than yesterday, streak is broken
    if current_date < yesterday:
        return 0

    # Start counting backwards
    expected_date = current_date
    for date in dates:
        if date == expected_date:
            streak += 1
            expected_date -= timedelta(days=1)
        else:
            break
            
    return streak

def update_user_streak(user):
    """
    Recalculates and updates the Sadhana streak on the UserProfile natively.
    """
    streak = calculate_sadhana_streak(user)
    if hasattr(user, 'profile'):
        user.profile.sadhana_streak = streak
        user.profile.save(update_fields=['sadhana_streak'])
    return streak
