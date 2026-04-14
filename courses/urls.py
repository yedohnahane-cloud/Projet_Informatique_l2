from django.urls import path
from .views import (
    subjects_page,
    courses_page,
    course_detail_page,
    chatbot_page,

    subjects_list,
    courses_list,
    course_detail_api,

    teacher_courses_list,
    create_course,
    teacher_course_detail,
    update_course,
    delete_course,
)

urlpatterns = [
    # Pages étudiant
    path("", subjects_page, name="subjects_page"),
    path("<int:subject_id>/chapters/", courses_page, name="courses_page"),
    path("chapters/<int:course_id>/view/", course_detail_page, name="course_detail_page"),
    path("chatbot/", chatbot_page, name="chatbot_page"),

    # API étudiant
    path("api/subjects/", subjects_list, name="subjects_list"),
    path("api/subjects/<int:subject_id>/courses/", courses_list, name="courses_list"),
    path("api/student/courses/<int:course_id>/", course_detail_api, name="course_detail_api"),

    # API professeur
    path("teacher/", teacher_courses_list, name="teacher_courses_list"),
    path("teacher/create/", create_course, name="create_course"),
    path("teacher/<int:course_id>/", teacher_course_detail, name="teacher_course_detail"),
    path("teacher/<int:course_id>/update/", update_course, name="update_course"),
    path("teacher/<int:course_id>/delete/", delete_course, name="delete_course"),
]