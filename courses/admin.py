from django.contrib import admin
from .models import Subject, Course, StudentCourseProgress


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("title", "teacher", "is_published", "created_at")
    search_fields = ("title",)
    list_filter = ("is_published", "teacher")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "teacher", "order", "is_published")
    search_fields = ("title",)
    list_filter = ("is_published", "teacher", "subject")


@admin.register(StudentCourseProgress)
class StudentCourseProgressAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "is_unlocked", "is_completed", "attempt_count")
    list_filter = ("is_unlocked", "is_completed")