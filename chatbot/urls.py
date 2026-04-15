from django.urls import path
from .views import test_llm

urlpatterns = [
    path("test-llm/", test_llm, name="test_llm"),
]