from django.contrib import admin
from .models import Quiz, Question, Choice, QuizAttempt


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "is_published", "created_at")
    list_filter = ("is_published",)
    search_fields = ("title", "course__title")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("quiz", "order", "text")
    ordering = ("quiz", "order")
    search_fields = ("text",)


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ("question", "text", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("text",)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("student", "quiz", "score", "attempt_number", "created_at")
    list_filter = ("quiz", "score", "attempt_number")
    search_fields = ("student__email", "quiz__title")