import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import call_llm


def test_llm(request):
    reply = call_llm("Explique Java en une phrase simple pour un débutant.")
    return JsonResponse(
        {"reply": reply},
        json_dumps_params={"ensure_ascii": False}
    )


@csrf_exempt
def send_message(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Méthode non autorisée"},
            status=405,
            json_dumps_params={"ensure_ascii": False}
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": "JSON invalide"},
            status=400,
            json_dumps_params={"ensure_ascii": False}
        )

    message = data.get("message", "").strip()

    if not message:
        return JsonResponse(
            {"error": "Message vide"},
            status=400,
            json_dumps_params={"ensure_ascii": False}
        )

    try:
        reply = call_llm(message)
        return JsonResponse(
            {
                "user_message": message,
                "assistant_reply": reply
            },
            json_dumps_params={"ensure_ascii": False}
        )
    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500,
            json_dumps_params={"ensure_ascii": False}
        )