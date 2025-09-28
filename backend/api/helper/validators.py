import requests
from dotenv import load_dotenv
import os
from openai import OpenAI, AuthenticationError, OpenAIError

def url_accessible(url):
    headers = {
        'User-Agent': (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        return response.ok and response.status_code == 200
    except requests.RequestException as e:
        print(f"Error: {e}")
        return False
    

def isStringEmpty(string):
    return not bool(string)

def check_open_ai(keyName:str):
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