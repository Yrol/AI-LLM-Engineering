from django.urls import path
from .views import open_ai_web_summarizer, open_ai_ask_anything, open_ai_create_brochure, open_ai_assistant, ollama_chat, ollama_create_brochure, ollama_web_summarizer

urlpatterns = [
    path('open_ai_websummarizer/', open_ai_web_summarizer, name='open_ai_websummarizer'),
    path('open_ai_askanything/', open_ai_ask_anything, name='open_ai_askanything'),
    path('open_ai_createbrochure/', open_ai_create_brochure, name='open_ai_createbrochure'),
    path('open_ai_assistant/', open_ai_assistant, name='open_ai_assistant'),
    path('ollama_chat/', ollama_chat, name='ollama_chat'),
    path('ollama_create_brochure/', ollama_create_brochure, name='ollama_create_brochure'),
    path('ollama_websummarizer/', ollama_web_summarizer, name='ollama_websummarizer')
]

