from django.urls import path
from .views import StudentGameListView

urlpatterns = [
    path("games/", StudentGameListView.as_view(), name="student-game-list"),
]