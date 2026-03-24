from django.utils import timezone
from .models import Course, StudentCourseProgress


def unlock_first_course_for_student(student):
    first_course = Course.objects.filter(is_published=True).order_by("order").first()

    if first_course:
        progress, created = StudentCourseProgress.objects.get_or_create(
            student=student,
            course=first_course,
            defaults={
                "is_unlocked": True,
                "unlocked_at": timezone.now()
            }
        )
        return progress

    return None