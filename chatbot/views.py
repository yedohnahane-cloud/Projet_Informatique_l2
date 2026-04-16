import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import ChatSession, ChatMessage
from .services import call_llm_with_history, call_llm


@require_GET
def test_llm(request):
    try:
        reply = call_llm("Dis bonjour en français.")
        return JsonResponse({"reply": reply})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@require_POST
@login_required
def create_session(request):
    try:
        data = json.loads(request.body)
        role = data.get("role", "student")

        session = ChatSession.objects.create(
            user=request.user,
            role=role
        )

        return JsonResponse({
            "session_id": session.id,
            "role": session.role
        })

    except Exception as e:
        return JsonResponse({
            "error": f"Erreur create_session : {str(e)}"
        }, status=500)


@require_POST
@login_required
def send_message(request):
    try:
        data = json.loads(request.body)
        session_id = data.get("session_id")
        message = data.get("message")

        if not session_id:
            return JsonResponse({"error": "session_id manquant"}, status=400)

        if not message:
            return JsonResponse({"error": "message manquant"}, status=400)

        session = get_object_or_404(ChatSession, id=session_id, user=request.user)

        ChatMessage.objects.create(
            session=session,
            sender="user",
            content=message
        )

        chat_messages = session.messages.all().order_by("created_at")
        assistant_reply = call_llm_with_history(chat_messages)

        ChatMessage.objects.create(
            session=session,
            sender="assistant",
            content=assistant_reply
        )

        return JsonResponse({
            "assistant_reply": assistant_reply
        })

    except Exception as e:
        return JsonResponse({
            "error": f"Erreur send_message : {str(e)}"
        }, status=500)


@require_GET
@login_required
def get_messages(request, session_id):
    try:
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)

        messages = session.messages.all().order_by("created_at").values(
            "sender", "content", "created_at"
        )

        return JsonResponse({
            "messages": list(messages)
        })

    except Exception as e:
        return JsonResponse({
            "error": f"Erreur get_messages : {str(e)}"
        }, status=500)