from django.urls import path
from .views import test_llm, send_message

urlpatterns = [
    path("test-llm/", test_llm, name="test_llm"),
    path("send-message/", send_message, name="send_message"),
]