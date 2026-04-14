from django.urls import path
from .views import courses_list, course_detail
from .views import (
    teacher_courses_list,
    teacher_course_detail,
    create_course,
    update_course,
    delete_course,
    subjects_page,
    courses_page,
    chatbot_page,
    subjects_list,
    courses_list,
    course_detail,
)
urlpatterns = [
    path("<int:course_id>/", course_detail, name="course_detail"),
    path("teacher/", teacher_courses_list, name="teacher_courses_list"),
    path("teacher/create/", create_course, name="create_course"),
    path("teacher/<int:course_id>/", teacher_course_detail, name="teacher_course_detail"),
    path("teacher/<int:course_id>/update/", update_course, name="update_course"),
    path("teacher/<int:course_id>/delete/", delete_course, name="delete_course"),
    path("", subjects_page, name="subjects_page"),
    path("page/", courses_page, name="courses_page"),
    path("chatbot/", chatbot_page, name="chatbot_page"),

    path("api/subjects/", subjects_list, name="subjects_list"),
    path("api/student/courses/", courses_list, name="courses_list"),
    path("api/student/courses/<int:course_id>/", course_detail, name="course_detail"),
]