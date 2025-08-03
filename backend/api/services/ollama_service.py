import requests
from openai import OpenAI
from ..helper.validators import isStringEmpty
from ..helper.constants import Method

endpoint = "http://ollama:11434/api/chat"

def ollama_ask_anything(model, messages, stream, raw_data, method):
    
    if isStringEmpty(model):
        raise ValueError("Invalid or empty model")
    
    if messages and isinstance(messages, list):
        
        role = messages[0].get('role', '')
        content = messages[0].get('content', '')
        
        if isStringEmpty(role):
            raise ValueError("Invalid or empty role")
        
        if isStringEmpty(content):
            raise ValueError("Invalid or empty content")
        
        if not isinstance(stream, bool):
            raise ValueError("Invalid or empty stream")
        
    if  method == Method.OPENAI.value: # making a call to Ollama through OpenAI by poiting to the ollama running in Docker
        ollama_via_openai = OpenAI(base_url='http://ollama:11434/v1', api_key='ollama')
        response = ollama_via_openai.chat.completions.create(
            model=model,
            messages=messages
        )
        return response.json()
    else: # making a call to Ollama running in Docker
        response = requests.post(endpoint, json=raw_data)
        return response.json()