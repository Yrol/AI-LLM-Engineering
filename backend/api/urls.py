from django.urls import path
from .views import web_summarizer, ask_anything

urlpatterns = [
    path('websummarizer/', web_summarizer, name='web_summarizer'),
    path('askanything/', ask_anything, name='ask_anything'),
]

