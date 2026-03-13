from django.urls import path
from .views import auth_page_view, signup_view, signin_view, logout_view

urlpatterns = [
    path("auth/", auth_page_view, name="auth_page"),
    path("signup/", signup_view, name="signup"),
    path("signin/", signin_view, name="signin"),
    path("logout/", logout_view, name="logout"),
]