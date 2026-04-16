import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Quiz
from .services import (
    can_start_quiz,
    calculate_score_and_errors,
    create_quiz_attempt,
    update_progress_after_attempt,
)
from courses .views import StudentCourseProgress

@login_required
def start_quiz(request, quiz_id):
    if request.user.role != "student":
        return JsonResponse({"error": "Accès réservé aux étudiants."}, status=403)

    try:
        quiz = Quiz.objects.prefetch_related("questions__choices").get(
            id=quiz_id,
            is_published=True
        )
    except Quiz.DoesNotExist:
        return JsonResponse({"error": "Quiz introuvable."}, status=404)

    allowed, result = can_start_quiz(request.user, quiz)

    if not allowed:
        return JsonResponse({
            "error": result,
            "redirect_to_result": result == "Nombre maximal de tentatives atteint."
        }, status=403)

    questions_data = []
    for question in quiz.questions.all():
        questions_data.append({
            "id": question.id,
            "text": question.text,
            "order": question.order,
            "choices": [
                {
                    "id": choice.id,
                    "text": choice.text,
                }
                for choice in question.choices.all()
            ]
        })

    return JsonResponse({
        "quiz_id": quiz.id,
        "quiz_title": quiz.title,
        "course_id": quiz.course.id,
        "questions": questions_data
    })


@login_required
def submit_quiz(request, quiz_id):
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée."}, status=405)

    if request.user.role != "student":
        return JsonResponse({"error": "Accès réservé aux étudiants."}, status=403)

    try:
        quiz = Quiz.objects.prefetch_related("questions__choices").get(
            id=quiz_id,
            is_published=True
        )
    except Quiz.DoesNotExist:
        return JsonResponse({"error": "Quiz introuvable."}, status=404)

    allowed, result = can_start_quiz(request.user, quiz)
    if not allowed:
        return JsonResponse({
            "error": result,
            "redirect_to_result": result == "Nombre maximal de tentatives atteint."
        }, status=403)

    try:
        body = json.loads(request.body)
        answers = body.get("answers", {})
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON invalide."}, status=400)

    score, errors = calculate_score_and_errors(quiz, answers)
    attempt = create_quiz_attempt(request.user, quiz, score, errors)
    progress, unlocked_next_course, next_course_id = update_progress_after_attempt(
        request.user,
        quiz,
        score
    )

    return JsonResponse({
        "message": "Quiz soumis avec succès.",
        "attempt_id": attempt.id,
        "score": score,
        "attempt_number": attempt.attempt_number,
        "is_completed": progress.is_completed,
        "attempt_count": progress.attempt_count,
        "errors": errors,
        "next_course_unlocked": unlocked_next_course,
        "next_course_id": next_course_id,
    }, status=200)


@login_required
def review_attempt(request, quiz_id):
    if request.user.role != "student":
        return JsonResponse({"error": "Accès réservé aux étudiants."}, status=403)

    quiz = Quiz.objects.filter(id=quiz_id).first()
    if not quiz:
        return JsonResponse({"error": "Quiz introuvable."}, status=404)

    attempt = quiz.attempts.filter(student=request.user).order_by("-attempt_number").first()
    if not attempt:
        return JsonResponse({"error": "Aucune tentative trouvée."}, status=404)

    try:
        progress = StudentCourseProgress.objects.get(
            student=request.user,
            course=quiz.course
        )
    except StudentCourseProgress.DoesNotExist:
        return JsonResponse({"error": "Progression introuvable."}, status=404)

    can_review = attempt.score >= 80 or progress.attempt_count >= 3

    if not can_review:
        return JsonResponse({
            "error": "Vous pourrez voir vos erreurs après avoir obtenu au moins 80% ou après 3 tentatives."
        }, status=403)

    return JsonResponse({
        "quiz_id": quiz.id,
        "quiz_title": quiz.title,
        "attempt_number": attempt.attempt_number,
        "score": attempt.score,
        "errors": attempt.error_summary,
        "created_at": attempt.created_at.strftime("%d/%m/%Y %H:%M"),
    })
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import QuizForm
from .models import Quiz, Question, Choice


@login_required
def create_quiz_page(request):
    if request.user.role != "teacher":
        return redirect("home")

    if request.method == "POST":
        form = QuizForm(request.POST)

        if form.is_valid():
            quiz = form.save()

            question_texts = request.POST.getlist("question_text[]")
            correct_answers = request.POST.getlist("question_correct[]")

            for index, question_text in enumerate(question_texts, start=1):
                if not question_text.strip():
                    continue

                question = Question.objects.create(
                    quiz=quiz,
                    text=question_text,
                    order=index
                )

                choice_values = request.POST.getlist(f"question_{index}_choice[]")
                correct_position = int(correct_answers[index - 1]) if index - 1 < len(correct_answers) else 1

                for choice_index, choice_text in enumerate(choice_values, start=1):
                    Choice.objects.create(
                        question=question,
                        text=choice_text,
                        is_correct=(choice_index == correct_position)
                    )

            return redirect("teacher_actions_page")
    else:
        form = QuizForm()

    return render(request, "quiz/formulaire-question.html", {"form": form})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quiz


@login_required
def quiz_page(request, quiz_id):
    if request.user.role != "student":
        return redirect("subjects_page")

    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)

    return render(request, "quiz/quiz-debut.html", {
        "quiz": quiz
    })


@login_required
def quiz_result_page(request, quiz_id):
    if request.user.role != "student":
        return redirect("subjects_page")

    quiz = get_object_or_404(Quiz, id=quiz_id)

    return render(request, "quiz/terminer-quiz-prof.html", {
        "quiz": quiz
    })

@login_required
def review_attempt_page(request, quiz_id):
    if request.user.role != "student":
        return redirect("subjects_page")

    quiz = Quiz.objects.filter(id=quiz_id).first()
    if not quiz:
        return redirect("subjects_page")

    return render(request, "quiz/review-attempt.html", {
        "quiz": quiz
    })

from django.views.decorators.http import require_POST
from courses.models import StudentCourseProgress


@login_required
@require_POST
def reset_quiz_attempts(request, quiz_id):
    if request.user.role != "student":
        return JsonResponse({"error": "Accès réservé aux étudiants."}, status=403)

    quiz = Quiz.objects.filter(id=quiz_id).first()
    if not quiz:
        return JsonResponse({"error": "Quiz introuvable."}, status=404)

    try:
        progress = StudentCourseProgress.objects.get(
            student=request.user,
            course=quiz.course
        )
    except StudentCourseProgress.DoesNotExist:
        return JsonResponse({"error": "Progression introuvable."}, status=404)

    # autorisé après 3 essais OU quiz validé
    if progress.attempt_count < 3 and not progress.is_completed:
        return JsonResponse({
            "error": "La réinitialisation n’est disponible qu’après 3 essais ou validation du quiz."
        }, status=403)

    progress.attempt_count = 0
    progress.save(update_fields=["attempt_count"])
