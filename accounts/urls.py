from django.urls import path
from .views import signup_view, signin_view, logout_view, leo_choisi_view, lucie_choisi_view

urlpatterns = [
    #path("auth/", auth_page_view, name="auth_page"),
    path("signup/", signup_view, name="signup"),
    path("signin/", signin_view, name="signin"),
    path("logout/", logout_view, name="logout"),
    path("leo/", leo_choisi_view, name="leo_choisi"),
    path("lucie/", lucie_choisi_view, name="lucie_choisi"),
    
]