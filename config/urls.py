from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def home_view(request):
    return HttpResponse("Bienvenue sur la page d'accueil")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home_view, name="home"),
    path("accounts/", include("accounts.urls")),
    path("courses/", include("courses.urls")),
    path("api/", include("games.urls")),
]