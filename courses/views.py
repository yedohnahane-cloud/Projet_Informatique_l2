from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Subject, Course, StudentCourseProgress
import json
from django.views.decorators.csrf import csrf_exempt


@login_required
def subjects_list(request):
    user = request.user

    if user.role != "student":
        return JsonResponse(
            {"error": "Accès réservé aux étudiants."},
            status=403
        )

    subjects = Subject.objects.filter(is_published=True).order_by("title")

    data = [
        {
            "id": subject.id,
            "title": subject.title,
            "description": subject.description or "",
        }
        for subject in subjects
    ]

    return JsonResponse({"subjects": data}, status=200)
@login_required
def courses_list(request):
    user = request.user

    if user.role != "student":
        return JsonResponse(
            {"error": "Accès réservé aux étudiants."},
            status=403
        )

    subject_id = request.GET.get("subject_id")

    courses = Course.objects.filter(is_published=True)

    if subject_id:
        courses = courses.filter(subject_id=subject_id)

    courses = courses.order_by("order")

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
            "subject_id": course.subject_id,
            "is_unlocked": progress.is_unlocked if progress else False,
            "is_completed": progress.is_completed if progress else False,
            "attempt_count": progress.attempt_count if progress else 0,
        })

    return JsonResponse({"courses": data}, status=200)
@login_required
def subjects_page(request):
    return render(request, "courses/subjects_list.html")


@login_required
def courses_page(request):
    return render(request, "courses/page_cours.html")


@login_required
def chatbot_page(request):
    return render(request, "courses/page_chatbot.html")

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
        "pdf_file": course.pdf_file.url if course.pdf_file else None,
        "order": course.order,
        "is_published": course.is_published,
        "is_unlocked": progress.is_unlocked,
        "is_completed": progress.is_completed,
        "attempt_count": progress.attempt_count,
    }

    return JsonResponse(data, status=200)

#//////////////////////////PROFESSEUR/////////////////////////////
@login_required
def teacher_courses_list(request):
    if request.user.role != "teacher":
        return JsonResponse(
            {"error": "Accès réservé aux professeurs."},
            status=403
        )

    courses = Course.objects.filter(teacher=request.user).order_by("order")

    data = [
        {
            "id": course.id,
            "title": course.title,
            "content": course.content,
            "order": course.order,
            "is_published": course.is_published,
            "created_at": course.created_at.isoformat(),
        }
        for course in courses
    ]

    return JsonResponse({"courses": data}, status=200)


@login_required
def teacher_course_detail(request, course_id):
    if request.user.role != "teacher":
        return JsonResponse(
            {"error": "Accès réservé aux professeurs."},
            status=403
        )

    try:
        course = Course.objects.get(id=course_id, teacher=request.user)
    except Course.DoesNotExist:
        return JsonResponse(
            {"error": "Cours introuvable."},
            status=404
        )

    return JsonResponse({
        "id": course.id,
        "title": course.title,
        "content": course.content,
        "order": course.order,
        "is_published": course.is_published,
        "created_at": course.created_at.isoformat(),
    }, status=200)


@csrf_exempt
@login_required
def create_course(request):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée."}, status=405)

    if request.user.role != "teacher":
        return JsonResponse(
            {"error": "Accès réservé aux professeurs."},
            status=403
        )

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON invalide."}, status=400)

    title = body.get("title")
    content = body.get("content")
    order = body.get("order")
    is_published = body.get("is_published", False)

    if not title or not content or order is None:
        return JsonResponse(
            {"error": "Les champs title, content et order sont obligatoires."},
            status=400
        )

    if Course.objects.filter(order=order).exists():
        return JsonResponse(
            {"error": "Un cours avec cet ordre existe déjà."},
            status=400
        )

    course = Course.objects.create(
        teacher=request.user,
        title=title,
        content=content,
        order=order,
        is_published=is_published
    )

    return JsonResponse({
        "message": "Cours créé avec succès.",
        "course": {
            "id": course.id,
            "title": course.title,
            "content": course.content,
            "order": course.order,
            "is_published": course.is_published,
            "created_at": course.created_at.isoformat(),
        }
    }, status=201)


@csrf_exempt
@login_required
def update_course(request, course_id):
    if request.method not in ["PUT", "PATCH"]:
        return JsonResponse({"error": "Méthode non autorisée."}, status=405)

    if request.user.role != "teacher":
        return JsonResponse(
            {"error": "Accès réservé aux professeurs."},
            status=403
        )

    try:
        course = Course.objects.get(id=course_id, teacher=request.user)
    except Course.DoesNotExist:
        return JsonResponse(
            {"error": "Cours introuvable."},
            status=404
        )

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON invalide."}, status=400)

    title = body.get("title", course.title)
    content = body.get("content", course.content)
    order = body.get("order", course.order)
    is_published = body.get("is_published", course.is_published)

    if order != course.order and Course.objects.filter(order=order).exists():
        return JsonResponse(
            {"error": "Un cours avec cet ordre existe déjà."},
            status=400
        )

    course.title = title
    course.content = content
    course.order = order
    course.is_published = is_published
    course.save()

    return JsonResponse({
        "message": "Cours mis à jour avec succès.",
        "course": {
            "id": course.id,
            "title": course.title,
            "content": course.content,
            "order": course.order,
            "is_published": course.is_published,
            "created_at": course.created_at.isoformat(),
        }
    }, status=200)


@csrf_exempt
@login_required
def delete_course(request, course_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Méthode non autorisée."}, status=405)

    if request.user.role != "teacher":
        return JsonResponse(
            {"error": "Accès réservé aux professeurs."},
            status=403
        )

    try:
        course = Course.objects.get(id=course_id, teacher=request.user)
    except Course.DoesNotExist:
        return JsonResponse(
            {"error": "Cours introuvable."},
            status=404
        )

    course.delete()

    return JsonResponse({
        "message": "Cours supprimé avec succès."
    }, status=200)