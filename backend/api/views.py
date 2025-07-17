from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .services.open_ai_sevice import summarise_web, open_ai_ask_anything
import json

@csrf_exempt
def web_summarizer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            systemInput = data.get('systemInput', '')
            userInput = data.get('userInput', '')
            website = data.get('website', '')
            return JsonResponse({'message': f'You sent: {summarise_web(systemInput, userInput, website)}'})
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
            return JsonResponse({'response': open_ai_ask_anything(message)})
        except ValueError as ve:
            return JsonResponse({'error': str(ve)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)
