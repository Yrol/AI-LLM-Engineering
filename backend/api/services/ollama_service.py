import requests
from ..helper.validators import isStringEmpty

endpoint = "http://ollama:11434/api/chat"

def ollama_ask_anything(model, messages, stream, raw_data):
    
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
        
    response = requests.post(endpoint, json=raw_data)
    return response.json()