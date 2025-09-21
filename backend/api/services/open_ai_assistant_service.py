import os
import json
from ..helper.website import Website
from ..helper.validators import url_accessible, isStringEmpty
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI, AuthenticationError, OpenAIError

class OpenAiAssistantService:
    
    def __init__(self):
        self.api_key_response = self.check_open_ai("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"
        self.openai = OpenAI()
        

    def open_ai_assistant(self, allMessages:str):

        if isinstance(self.api_key_response, str):
            raise ValueError(self.api_key_response)
        else:
            messages = [{"role": "system", "content": self.get_system_prompt_for_ai_assistant()}] + allMessages
            response = self.openai.chat.completions.create(
                model=self.model, 
                messages=messages
            )
            print(response.choices[0].message.content)
            return response.choices[0].message.content
        
    def get_system_prompt_for_ai_assistant(self):
         return "You are a helpful assistant"   
     
    def check_open_ai(self, keyName:str):
        load_dotenv(override=True)
        api_key = os.getenv(keyName)

        if not api_key:
            return "No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!"
        elif not api_key.startswith("sk-proj-"):
            return "An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook"
        elif api_key.strip() != api_key:
            return "An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook"

        try:
            client = OpenAI(api_key=api_key)
            client.models.list()
            return True
        except AuthenticationError:
            return "API key is invalid or unauthorized."
        except OpenAIError as e:
            return f"API key check failed due to an OpenAI error: {str(e)}"
        except Exception as e:
            return f"Unexpected error while checking API key: {str(e)}"