from django.shortcuts import render
from django.http import JsonResponse
from .services import call_llm

def test_llm(request):
    reply = call_llm("Explique Java en une phrase simple pour un débutant.")
    return JsonResponse({"reply": reply})