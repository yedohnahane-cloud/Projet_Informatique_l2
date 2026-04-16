from django.urls import path
from .views import test_llm, create_session, send_message, get_messages

urlpatterns = [
    path("test-llm/", test_llm, name="test_llm"),
    path("create-session/", create_session, name="create_session"),
    path("send-message/", send_message, name="send_message"),
    path("sessions/<int:session_id>/messages/", get_messages, name="get_messages"),
    
]