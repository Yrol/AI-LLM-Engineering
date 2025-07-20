import requests
import os
from ..helper.website import Website
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI
from openai import AuthenticationError, OpenAIError


def summarise_web(systemInput, webUrl):

    api_key_respose = check_open_ai("OPENAI_API_KEY")

    if isinstance(api_key_respose, str):
        raise ValueError(api_key_respose)
    if not url_accessible(webUrl):
        raise ValueError("Invalid website URL")
    else:
        website = Website(webUrl)
        openai = OpenAI()
        response = openai.chat.completions.create(
            model="gpt-4o-mini", messages=messages_for(website, systemInput)
        )
        return response.choices[0].message.content
        
def open_ai_ask_anything(message):
    api_key_respose = check_open_ai("OPENAI_API_KEY")
    openai = OpenAI()

    if isinstance(api_key_respose, str):
        raise ValueError(api_key_respose)
    else:
        response = openai.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
please provide a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt


def messages_for(website, system_prompt):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)},
    ]


def url_accessible(url):
    try:
        response = requests.get(url, timeout=5)
        return True
    except requests.RequestException:
        return False


def check_open_ai(keyName):
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
