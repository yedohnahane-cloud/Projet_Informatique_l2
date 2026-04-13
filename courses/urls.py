from django.urls import path
from .views import courses_list, course_detail
from .views import (
    teacher_courses_list,
    teacher_course_detail,
    create_course,
    update_course,
    delete_course,
)
urlpatterns = [
    path("", courses_list, name="courses_list"),
    path("<int:course_id>/", course_detail, name="course_detail"),
    path("teacher/", teacher_courses_list, name="teacher_courses_list"),
    path("teacher/create/", create_course, name="create_course"),
    path("teacher/<int:course_id>/", teacher_course_detail, name="teacher_course_detail"),
    path("teacher/<int:course_id>/update/", update_course, name="update_course"),
    path("teacher/<int:course_id>/delete/", delete_course, name="delete_course"),
]