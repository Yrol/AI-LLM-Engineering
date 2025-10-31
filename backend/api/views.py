from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .services.open_ai_service import OpenAiService
from .services.open_ai_assistant_service import OpenAiAssistantService
from .services.open_ai_ticketing_assistant_service import OpenAiTicketingAssistantService
from .services.ollama_service import OllamaService
from .services.hugging_face_pipeline_service import HuggingFacePipelineService
from .helper.constants import ALLOWED_METHODS, DEFAULT_METHOD
import json

openAiservice = OpenAiService()
openAiAssistantService = OpenAiAssistantService()
openAiTicketingAssistantService = OpenAiTicketingAssistantService()
ollamaService = OllamaService()
huggingFaceService = HuggingFacePipelineService()

@csrf_exempt
def open_ai_web_summarizer(request):
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
def open_ai_ask_anything(request):
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
def open_ai_create_brochure(request):
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
def open_ai_assistant(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            history = data.get('messages','')
            prompt = data.get('prompt','')
            if isinstance(history, list):
                reply = openAiAssistantService.open_ai_assistant(history, prompt)
            else:
                history = []
            return JsonResponse({"reply": reply}, safe=False)
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)


@csrf_exempt
def open_ai_ticketing_assistant(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            history = data.get('messages','')
            prompt = data.get('prompt','')
            if isinstance(history, list):
                reply = openAiTicketingAssistantService.open_ai_ticketing_assistant(history, prompt)
            else:
                history = []
            return JsonResponse({"reply": reply}, safe=False)
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

@csrf_exempt
def ollama_web_summarizer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            systemInput = data.get('systemInput', '')
            website = data.get('website', '')
            return JsonResponse({'message': f'{ollamaService.ollama_summarise_web(systemInput, website)}'})
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)

@csrf_exempt
def huggingface_named_entity_analysis(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            return JsonResponse({'message': f'{huggingFaceService.named_entity_analysis(prompt)}'})
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)


@csrf_exempt
def huggingface_sentiment_analysis(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            prompt = data.get('prompt', '')
            return JsonResponse({'message': f'{huggingFaceService.sentiment_analysis(prompt)}'})
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)