from django.db import models
from django.conf import settings
from courses.models import Course


class Quiz(models.Model):
    course = models.OneToOneField(
        Course,
        on_delete=models.CASCADE,
        related_name="quiz"
    )
    title = models.CharField(max_length=255)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions"
    )
    text = models.TextField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ["order"]
        unique_together = ("quiz", "order")

    def __str__(self):
        return f"Question {self.order} - {self.quiz.title}"


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="choices"
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class QuizAttempt(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
        limit_choices_to={"role": "student"}
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="attempts"
    )
    score = models.FloatField()
    attempt_number = models.PositiveIntegerField()
    error_summary = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("student", "quiz", "attempt_number")

    def __str__(self):
        return f"{self.student.email} - {self.quiz.title} - Tentative {self.attempt_number}"