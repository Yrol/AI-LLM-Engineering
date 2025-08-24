from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .services.open_ai_service import OpenAIService
from .services.ollama_service import OllamaService
from .helper.constants import ALLOWED_METHODS, DEFAULT_METHOD
import json

openAiservice = OpenAIService()
ollamaService = OllamaService()

@csrf_exempt
def web_summarizer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            systemInput = data.get('systemInput', '')
            website = data.get('website', '')
            return JsonResponse({'message': f'{openAiservice.open_ai_summarise_web(systemInput, website)}'})
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)

@csrf_exempt
def ask_anything(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message')
            return JsonResponse({'response': openAiservice.open_ai_ask_anything(message)})
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)

@csrf_exempt
def ollama_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            model = data.get('model', '')
            messages = data.get('messages', [])
            stream = data.get('stream', False)
            method_raw = data.get('method', '').lower()
            method = method_raw if method_raw in ALLOWED_METHODS else DEFAULT_METHOD.value
            return JsonResponse(ollamaService.ollama_ask_anything(model, messages, stream, data, method))
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)


@csrf_exempt
def create_brochure(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            company_name = data.get('companyName', '')
            website_url = data.get('websiteUrl', '')
            return JsonResponse(openAiservice.open_ai_create_brochure(company_name, website_url), safe=False)
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)

@csrf_exempt
def ollama_create_brochure(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            company_name = data.get('companyName', '')
            website_url = data.get('websiteUrl', '')
            return JsonResponse(ollamaService.ollama_create_brochure(company_name, website_url), safe=False)
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)