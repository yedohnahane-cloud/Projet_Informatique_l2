from django.db import models
from django.conf import settings

from django.conf import settings
from django.db import models


class Subject(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subjects"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Course(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    pdf_file = models.FileField(upload_to="courses/pdfs/", blank=True, null=True)
    order = models.PositiveIntegerField(unique=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(Subject,
    on_delete=models.CASCADE,
    related_name="courses",
    null=True,
    blank=True
)

    def __str__(self):
        return f"{self.order} - {self.title}"

class StudentCourseProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_progress",
        limit_choices_to={"role": "student"}
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="student_progress"
    )
    is_unlocked = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    attempt_count = models.PositiveIntegerField(default=0)
    unlocked_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("student", "course")
        ordering = ["course__order"]

    def __str__(self):
        return f"{self.student.email} - {self.course.title}"
    
    #