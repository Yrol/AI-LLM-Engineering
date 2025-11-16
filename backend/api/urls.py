from django.urls import path
from .views import open_ai_web_summarizer, open_ai_ask_anything,open_ai_ticketing_assistant,open_ai_create_brochure, open_ai_assistant, ollama_chat, ollama_create_brochure, ollama_web_summarizer, huggingface_named_entity_analysis, huggingface_sentiment_analysis, huggingface_question_answering, huggingface_translator, huggingface_classification, huggingface_text_generation

urlpatterns = [
    path('open_ai_websummarizer/', open_ai_web_summarizer, name='open_ai_websummarizer'),
    path('open_ai_askanything/', open_ai_ask_anything, name='open_ai_askanything'),
    path('open_ai_ticketing_assistant/', open_ai_ticketing_assistant, name='open_ai_ticketing_assistant'),
    path('open_ai_createbrochure/', open_ai_create_brochure, name='open_ai_createbrochure'),
    path('open_ai_assistant/', open_ai_assistant, name='open_ai_assistant'),
    path('ollama_chat/', ollama_chat, name='ollama_chat'),
    path('ollama_create_brochure/', ollama_create_brochure, name='ollama_create_brochure'),
    path('ollama_websummarizer/', ollama_web_summarizer, name='ollama_websummarizer'),
    path('huggingface_named_entity_analysis/', huggingface_named_entity_analysis, name='huggingface_named_entity_analysis'),
    path('huggingface_sentiment_analysis/', huggingface_sentiment_analysis, name='huggingface_sentiment_analysis'),
    path('huggingface_question_answering/', huggingface_question_answering, name='huggingface_question_answering'),
    path('huggingface_translator/', huggingface_translator, name='huggingface_translator'),
    path('huggingface_classification/', huggingface_classification, name='huggingface_classification'),
    path('huggingface_text_generation/', huggingface_text_generation, name='huggingface_text_generation')
]

