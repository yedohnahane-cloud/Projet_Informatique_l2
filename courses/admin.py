from django.contrib import admin
from .models import Course, StudentCourseProgress


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "order", "is_published", "created_at")
    list_filter = ("is_published", "teacher")
    search_fields = ("title", "content")
    ordering = ("order",)


@admin.register(StudentCourseProgress)
class StudentCourseProgressAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "course",
        "is_unlocked",
        "is_completed",
        "attempt_count",
        "unlocked_at",
        "completed_at",
    )
    list_filter = ("is_unlocked", "is_completed")
    search_fields = ("student__email", "course__title")
    ordering = ("course__order",)