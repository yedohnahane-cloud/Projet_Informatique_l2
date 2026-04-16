import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)


def call_llm(prompt):
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    return response.text


def build_messages_for_llm(chat_messages):
    prompt = (
        "Tu es un assistant pédagogique spécialisé en Java. "
        "Réponds clairement, simplement, et en français.\n\n"
    )

    for msg in chat_messages:
        if msg.sender == "user":
            prompt += f"Utilisateur: {msg.content}\n"
        elif msg.sender == "assistant":
            prompt += f"Assistant: {msg.content}\n"
        elif msg.sender == "system":
            prompt += f"Système: {msg.content}\n"

    prompt += "Assistant: "
    return prompt


def call_llm_with_history(chat_messages):
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = build_messages_for_llm(chat_messages)
    response = model.generate_content(prompt)
    return response.text