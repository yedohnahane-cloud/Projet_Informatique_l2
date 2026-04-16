from django.urls import path
from django.urls import path
from .views import (
    start_quiz,
    submit_quiz,
    create_quiz_page,
    review_attempt,
    quiz_page,
    quiz_result_page,
    review_attempt_page, 
    reset_quiz_attempts
)
urlpatterns = [
    path("<int:quiz_id>/start/", start_quiz, name="start_quiz"),
    path("<int:quiz_id>/submit/", submit_quiz, name="submit_quiz"),
    path("<int:quiz_id>/review/", review_attempt, name="review_attempt"),

    path("<int:quiz_id>/play/", quiz_page, name="quiz_page"),
    path("<int:quiz_id>/result/", quiz_result_page, name="quiz_result_page"),

    path("teacher/create/", create_quiz_page, name="create_quiz_page"),
    path("<int:quiz_id>/review-page/", review_attempt_page, name="review_attempt_page"),
    path("<int:quiz_id>/reset-attempts/", reset_quiz_attempts, name="reset_quiz_attempts"),
]
