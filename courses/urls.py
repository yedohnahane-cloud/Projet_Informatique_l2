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
    teacher_actions_page,
    create_subject_page,
    create_course_page,
    teacher_courses_list_page,
    games_page
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
    path("games/", games_page, name="games_page"),

    # API professeur
    path("teacher/", teacher_courses_list, name="teacher_courses_list"),
    path("teacher/create/", create_course, name="create_course"),
    path("teacher/<int:course_id>/", teacher_course_detail, name="teacher_course_detail"),
    path("teacher/<int:course_id>/update/", update_course, name="update_course"),
    path("teacher/<int:course_id>/delete/", delete_course, name="delete_course"),
    path("teacher/actions/", teacher_actions_page, name="teacher_actions_page"),
    path("teacher/subjects/create/", create_subject_page, name="create_subject_page"),
    path("teacher/courses/create/", create_course_page, name="create_course_page"),
    path("teacher/my-courses/", teacher_courses_list_page, name="teacher_courses_list_page"),
]