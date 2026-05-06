import random
from subjects.models import Topic
from exams.models import Exam

SANSKRIT_QUOTES = [
    "विद्या धनं सर्व धन प्रधानम्। (Knowledge is the ultimate wealth)",
    "उद्यमेन हि सिध्यन्ति कार्याणि न मनोरथैः। (Efforts bring success, not mere wishes)",
    "आलस्यं हि मनुष्याणां शरीरस्थो महान् रिपुः। (Laziness is the greatest enemy residing in the body)",
    "योगः कर्मसु कौशलम्। (Yoga is excellence in action)"
]

def generate_ai_suggestion(user):
    """
    Basic AI logic generating study suggestions based on heuristics.
    """
    next_exam = Exam.objects.for_user(user).upcoming().first()
    
    if next_exam and next_exam.countdown_days < 7:
        return {
            "type": "alert",
            "message": f"Shishya, your {next_exam.name} Pariksha is in {next_exam.countdown_days} days! Shift focus entirely to {next_exam.subject.name} mocks.",
            "quote": random.choice(SANSKRIT_QUOTES)
        }

    weak_topic = Topic.objects.filter(subject__user=user, is_completed=False).order_by('confidence_level').first()
    if weak_topic:
        return {
            "type": "focus",
            "message": f"Your confidence in '{weak_topic.name}' is critically low ({weak_topic.confidence_level}%). A 45-minute deep Adhyayan session is recommended.",
            "quote": random.choice(SANSKRIT_QUOTES)
        }
    
    return {
        "type": "general",
        "message": "You have achieved exceptional balance across your Vishay. Proceed with your standard routine.",
        "quote": random.choice(SANSKRIT_QUOTES)
    }

def generate_daily_plan(user):
    """
    Smart daily planner logic prioritizing exams and weak topics natively.
    """
    plan = []
    
    # Task 1: Imminent Exam
    next_exam = Exam.objects.for_user(user).upcoming().first()
    if next_exam:
        plan.append({
            "task": f"Pariksha Review: {next_exam.subject.name}",
            "priority": "High",
            "estimated_minutes": 60,
            "category": "Exam Prep"
        })

    # Task 2: Weakest Link
    weak_topic = Topic.objects.filter(subject__user=user, is_completed=False).order_by('confidence_level').first()
    if weak_topic:
        plan.append({
            "task": f"Mastery Focus: {weak_topic.name}",
            "priority": "Medium",
            "estimated_minutes": 45,
            "category": "Weakness Targeting"
        })

    # Task 3: Standard Progression
    exclude_id = weak_topic.id if weak_topic else None
    pending_topic = Topic.objects.filter(
        subject__user=user, is_completed=False
    ).exclude(id=exclude_id).order_by('-created_at').first()
    
    if pending_topic:
        plan.append({
            "task": f"New Adhyayan: {pending_topic.name}",
            "priority": "Standard",
            "estimated_minutes": 30,
            "category": "Curriculum Progress"
        })

    return plan
