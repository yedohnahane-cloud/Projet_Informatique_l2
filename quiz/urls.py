from django.urls import path
from .views import start_quiz, submit_quiz,create_quiz_page, review_attempt

urlpatterns = [
    path("<int:quiz_id>/start/", start_quiz, name="start_quiz"),
    path("<int:quiz_id>/submit/", submit_quiz, name="submit_quiz"),
    path("<int:quiz_id>/review/", review_attempt, name="review_attempt"),
    path("teacher/create/", create_quiz_page, name="create_quiz_page"),
]