from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static
from . import views




urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home_view, name="home"),
    path("about/", views.about_us_view, name="about_us"),
    path("accounts/", include("accounts.urls")),
    path("courses/", include("courses.urls")),
    path("quiz/", include("quiz.urls")),
    path("api/", include("games.urls")),
    path("chatbot/", include("chatbot.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


