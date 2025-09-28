from ..helper.validators import check_open_ai
from openai import OpenAI

class OpenAiAssistantService:
    
    def __init__(self):
        self.api_key_response = check_open_ai("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"
        self.openai = OpenAI()
        
    def open_ai_assistant(self, messages:str, prompt:str):

        if isinstance(self.api_key_response, str):
            raise ValueError(self.api_key_response)
        else:
            messages = [{"role": "system", "content": prompt}] + messages
            response = self.openai.chat.completions.create(
                model=self.model, 
                messages=messages
            )
            print(response.choices[0].message.content)
            return response.choices[0].message.content