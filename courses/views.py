from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Course, StudentCourseProgress


@login_required
def courses_list(request):
    user = request.user

    if user.role != "student":
        return JsonResponse(
            {"error": "Accès réservé aux étudiants."},
            status=403
        )

    courses = Course.objects.filter(is_published=True).order_by("order")
    progress_map = {
        progress.course_id: progress
        for progress in StudentCourseProgress.objects.filter(student=user)
    }

    data = []
    for course in courses:
        progress = progress_map.get(course.id)

        data.append({
            "id": course.id,
            "title": course.title,
            "order": course.order,
            "is_unlocked": progress.is_unlocked if progress else False,
            "is_completed": progress.is_completed if progress else False,
            "attempt_count": progress.attempt_count if progress else 0,
        })

    return JsonResponse({"courses": data}, status=200)


@login_required
def course_detail(request, course_id):
    user = request.user

    if user.role != "student":
        return JsonResponse(
            {"error": "Accès réservé aux étudiants."},
            status=403
        )

    try:
        progress = StudentCourseProgress.objects.select_related("course").get(
            student=user,
            course_id=course_id,
            course__is_published=True
        )
    except StudentCourseProgress.DoesNotExist:
        return JsonResponse(
            {"error": "Cours introuvable ou progression inexistante."},
            status=404
        )

    if not progress.is_unlocked:
        return JsonResponse(
            {"error": "Ce cours est verrouillé."},
            status=403
        )

    course = progress.course

    data = {
        "id": course.id,
        "title": course.title,
        "content": course.content,
        "order": course.order,
        "is_published": course.is_published,
        "is_unlocked": progress.is_unlocked,
        "is_completed": progress.is_completed,
        "attempt_count": progress.attempt_count,
    }

    return JsonResponse(data, status=200)