from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Subject, Course, StudentCourseProgress
import json
from django.views.decorators.csrf import csrf_exempt


# =========================
# PAGES ETUDIANT
# =========================

@login_required
def subjects_page(request):
    return render(request, "courses/subjects_list.html")


@login_required
def courses_page(request, subject_id):
    return render(request, "courses/coursprincipal.html", {
        "subject_id": subject_id
    })


@login_required
def course_detail_page(request, course_id):
    return render(request, "courses/page_cours.html", {
        "course_id": course_id
    })


@login_required
def chatbot_page(request):
    return render(request, "courses/page_chatbot.html")


# =========================
# API ETUDIANT
# =========================

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
def courses_list(request, subject_id):
    user = request.user

    courses = Course.objects.filter(
        is_published=True,
        subject_id=subject_id
    ).order_by("order")

    # Prof ou admin : tout est accessible
    if user.is_superuser or user.role == "teacher":
        data = [
            {
                "id": course.id,
                "title": course.title,
                "content": course.content,
                "order": course.order,
                "subject_id": course.subject_id,
                "is_unlocked": True,
                "is_completed": False,
                "attempt_count": 0,
            }
            for course in courses
        ]
        return JsonResponse({"courses": data}, status=200)

    # Étudiant uniquement à partir d’ici
    if user.role != "student":
        return JsonResponse(
            {"error": "Accès non autorisé."},
            status=403
        )

    # Récupération progression existante
    progress_qs = StudentCourseProgress.objects.filter(
        student=user,
        course__subject_id=subject_id
    ).select_related("course")

    progress_map = {
        progress.course_id: progress
        for progress in progress_qs
    }

    # Si aucune progression n'existe encore pour ce subject,
    # on l'initialise automatiquement
    if not progress_map and courses.exists():
        progress_objects = []

        for course in courses:
            progress_objects.append(
                StudentCourseProgress(
                    student=user,
                    course=course,
                    is_unlocked=(course.order == 1),
                    is_completed=False,
                    attempt_count=0,
                )
            )

        StudentCourseProgress.objects.bulk_create(progress_objects)

        progress_qs = StudentCourseProgress.objects.filter(
            student=user,
            course__subject_id=subject_id
        ).select_related("course")

        progress_map = {
            progress.course_id: progress
            for progress in progress_qs
        }

    data = []
    for course in courses:
        progress = progress_map.get(course.id)

        data.append({
            "id": course.id,
            "title": course.title,
            "content": course.content,
            "order": course.order,
            "subject_id": course.subject_id,
            "is_unlocked": progress.is_unlocked if progress else False,
            "is_completed": progress.is_completed if progress else False,
            "attempt_count": progress.attempt_count if progress else 0,
        })

    return JsonResponse({"courses": data}, status=200)

@login_required
def course_detail_api(request, course_id):
    user = request.user

    try:
        course = Course.objects.get(id=course_id, is_published=True)
    except Course.DoesNotExist:
        return JsonResponse(
            {"error": "Chapitre introuvable."},
            status=404
        )

    # Prof ou admin : accès total
    if user.is_superuser or user.role == "teacher":
        return JsonResponse({
            "id": course.id,
            "title": course.title,
            "content": course.content,
            "pdf_file": course.pdf_file.url if course.pdf_file else None,
            "order": course.order,
            "is_published": course.is_published,
            "is_unlocked": True,
            "is_completed": False,
            "attempt_count": 0,
        }, status=200)

    if user.role != "student":
        return JsonResponse(
            {"error": "Accès non autorisé."},
            status=403
        )

    progress, created = StudentCourseProgress.objects.get_or_create(
        student=user,
        course=course,
        defaults={
            "is_unlocked": course.order == 1,
            "is_completed": False,
            "attempt_count": 0,
        }
    )

    if not progress.is_unlocked:
        return JsonResponse(
            {"error": "Ce chapitre est verrouillé."},
            status=403
        )

    return JsonResponse({
        "id": course.id,
        "title": course.title,
        "content": course.content,
        "pdf_file": course.pdf_file.url if course.pdf_file else None,
        "order": course.order,
        "is_published": course.is_published,
        "is_unlocked": progress.is_unlocked,
        "is_completed": progress.is_completed,
        "attempt_count": progress.attempt_count,
    }, status=200)
# =========================
# API PROFESSEUR
# =========================

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
    subject_id = body.get("subject_id")

    if not title or not content or order is None or not subject_id:
        return JsonResponse(
            {"error": "Les champs title, content, order et subject_id sont obligatoires."},
            status=400
        )

    if Course.objects.filter(order=order, subject_id=subject_id).exists():
        return JsonResponse(
            {"error": "Un chapitre avec cet ordre existe déjà dans ce cours."},
            status=400
        )

    course = Course.objects.create(
        teacher=request.user,
        subject_id=subject_id,
        title=title,
        content=content,
        order=order,
        is_published=is_published
    )

    return JsonResponse({
        "message": "Chapitre créé avec succès.",
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

    if order != course.order and Course.objects.filter(
        order=order,
        subject_id=course.subject_id
    ).exclude(id=course.id).exists():
        return JsonResponse(
            {"error": "Un chapitre avec cet ordre existe déjà dans ce cours."},
            status=400
        )

    course.title = title
    course.content = content
    course.order = order
    course.is_published = is_published
    course.save()

    return JsonResponse({
        "message": "Chapitre mis à jour avec succès.",
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
        "message": "Chapitre supprimé avec succès."
    }, status=200)