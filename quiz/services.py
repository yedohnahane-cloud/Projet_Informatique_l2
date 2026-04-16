from django.utils import timezone
from .models import QuizAttempt
from courses.models import StudentCourseProgress, Course


def calculate_score_and_errors(quiz, answers):
    """
    answers = {
        "question_id": choice_id
    }
    """
    questions = quiz.questions.prefetch_related("choices").all()
    total_questions = questions.count()

    if total_questions == 0:
        return 0, []

    correct_count = 0
    errors = []

    for question in questions:
        correct_choice = question.choices.filter(is_correct=True).first()
        selected_choice_id = answers.get(str(question.id)) or answers.get(question.id)
        selected_choice = question.choices.filter(id=selected_choice_id).first()

        if selected_choice and correct_choice and selected_choice.id == correct_choice.id:
            correct_count += 1
        else:
            errors.append({
                "question_id": question.id,
                "question_text": question.text,
                "selected_choice": selected_choice.text if selected_choice else None,
                "correct_choice": correct_choice.text if correct_choice else None,
            })

    score = (correct_count / total_questions) * 100
    return round(score, 2), errors


def get_next_attempt_number(student, quiz):
    last_attempt = QuizAttempt.objects.filter(
        student=student,
        quiz=quiz
    ).order_by("-attempt_number").first()

    if last_attempt:
        return last_attempt.attempt_number + 1
    return 1


def can_start_quiz(student, quiz):
    try:
        progress = StudentCourseProgress.objects.get(
            student=student,
            course=quiz.course
        )
    except StudentCourseProgress.DoesNotExist:
        return False, "Progression introuvable."

    if not progress.is_unlocked:
        return False, "Ce cours est verrouillé."

    if not quiz.is_published:
        return False, "Ce quiz n'est pas publié."

    if progress.attempt_count >= 3:
        return False, "Nombre maximal de tentatives atteint."

    return True, progress


def create_quiz_attempt(student, quiz, score, errors):
    attempt_number = get_next_attempt_number(student, quiz)

    attempt = QuizAttempt.objects.create(
        student=student,
        quiz=quiz,
        score=score,
        attempt_number=attempt_number,
        error_summary=errors
    )

    return attempt


def update_progress_after_attempt(student, quiz, score):
    progress = StudentCourseProgress.objects.get(
        student=student,
        course=quiz.course
    )

    progress.attempt_count += 1

    unlocked_next_course = False
    next_course_id = None

    print("=== DEBUG update_progress_after_attempt ===")
    print("student:", student.email)
    print("course:", quiz.course.id, quiz.course.title)
    print("score:", score)
    print("attempt_count before save:", progress.attempt_count)

    if score >= 80:
        progress.is_completed = True
        if not progress.completed_at:
            progress.completed_at = timezone.now()
        progress.save()

        print("quiz réussi, on débloque le suivant")
        unlocked_next_course, next_course_id = unlock_next_course(student, quiz.course)

    elif progress.attempt_count >= 3:
        progress.save()

        print("3 essais atteints, on débloque le suivant")
        unlocked_next_course, next_course_id = unlock_next_course(student, quiz.course)

    else:
        progress.save()
        print("pas encore validé, pas de déblocage")

    print("unlocked_next_course:", unlocked_next_course)
    print("next_course_id:", next_course_id)

    return progress, unlocked_next_course, next_course_id

def unlock_next_course(student, current_course):
    next_course = Course.objects.filter(
        subject=current_course.subject,
        is_published=True,
        order__gt=current_course.order
    ).order_by("order").first()

    print("=== DEBUG unlock_next_course ===")
    print("current_course:", current_course.id, current_course.title, current_course.order)
    print("subject:", current_course.subject_id)
    print("next_course found:", next_course.id if next_course else None)

    if not next_course:
        return False, None

    next_progress, created = StudentCourseProgress.objects.get_or_create(
        student=student,
        course=next_course,
        defaults={
            "is_unlocked": True,
            "unlocked_at": timezone.now()
        }
    )

    print("next_progress created:", created)
    print("before unlock:", next_progress.is_unlocked)

    if not next_progress.is_unlocked:
        next_progress.is_unlocked = True
        next_progress.unlocked_at = timezone.now()
        next_progress.save()

    print("after unlock:", next_progress.is_unlocked)

    return True, next_course.id