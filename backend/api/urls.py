from django.urls import path
from .views import web_summarizer, ask_anything, ollama_chat, create_brochure, ollama_create_brochure

urlpatterns = [
    path('websummarizer/', web_summarizer, name='web_summarizer'),
    path('askanything/', ask_anything, name='ask_anything'),
    path('ollamachat/', ollama_chat, name='ollama_chat'),
    path('ollama_create_brochure/', ollama_create_brochure, name='ollama_create_brochure'),
    path('createbrochure/', create_brochure, name='create_brochure')
]

