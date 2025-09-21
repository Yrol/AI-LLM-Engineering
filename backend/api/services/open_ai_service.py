import os
import json
from ..helper.website import Website
from ..helper.validators import url_accessible, isStringEmpty
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from openai import OpenAI, AuthenticationError, OpenAIError

class OpenAiService:
    
    def __init__(self):
        self.api_key_response = self.check_open_ai("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"
        self.openai = OpenAI()

    def open_ai_summarise_web(self, systemInput:str, webUrl:str):

        if isinstance(self.api_key_response, str):
            raise ValueError(self.api_key_response)
        if not url_accessible(webUrl):
            raise ValueError("Invalid website URL")
        if isStringEmpty(systemInput):
            raise ValueError("Invalid or empty System Input") 
        else:
            website = Website(webUrl)
            response = self.openai.chat.completions.create(
                model=self.model, 
                messages=self.messages_for(website, systemInput)
            )
            return response.choices[0].message.content
        
            
    def open_ai_ask_anything(self, message:str):

        if isinstance(self.api_key_response, str):
            raise ValueError(self.api_key_response)
        else:
            response = self.openai.chat.completions.create(
                model=self.model, messages=[{"role": "user", "content": message}]
            )
            return response.choices[0].message.content


    def get_user_prompt_for_summarizer(self, website:Website):
        user_prompt = f"You are looking at a website titled {website.title}"
        user_prompt += "\nThe contents of this website is as follows; \
    please provide a short summary of this website in markdown. \
    If it includes news or announcements, then summarize these too.\n\n"
        user_prompt += website.text
        return user_prompt


    def get_system_prompt_for_brochure(self):
        link_system_prompt = "You are provided with a list of links found on a webpage. \
                                You are able to decide which of the links would be most relevant to include in a brochure about the company, \
                                such as links to an About page, or a Company page, or Careers/Jobs pages.\n"
        link_system_prompt += "You should respond in JSON as in this example:"
        link_system_prompt += """
                            {
                                "links": [
                                    {"type": "about page", "url": "https://full.url/goes/here/about"},
                                    {"type": "careers page": "url": "https://another.full.url/careers"}
                                ]
                            }
                            """
        return link_system_prompt


    def get_links_user_prompt(self, website:Website):
        user_prompt = f"Here is the list of links on the website of {website.url} - "
        user_prompt += "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. \
    Do not include Terms of Service, Privacy, email links.\n"
        user_prompt += "Links (some might be relative links):\n"
        user_prompt += "\n".join(website.links)
        return user_prompt


    def get_links(self, url:str):
        website = Website(url)
        response = self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.get_system_prompt_for_brochure()},
                {"role": "user", "content": self.get_links_user_prompt(website)}
            ],
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content
        print(response)
        return json.loads(result)

    def get_all_details(self, url:str):
        result = "Landing page:\n"
        result += Website(url).get_contents()
        links = self.get_links(url)
        # print("Found links:", links)
        for link in links["links"]:
            result += f"\n\n{link['type']}\n"
            result += Website(link["url"]).get_contents()
        return result

    def get_brochure_user_prompt(self, company_name:str, url:str):
        user_prompt = f"You are looking at a company called: {company_name}\n"
        user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
        user_prompt += self.get_all_details(url)
        user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
        return user_prompt

    def open_ai_create_brochure(self, company_name:str, url:str):
        
        if isinstance(self.api_key_response, str):
            raise ValueError(self.api_key_response)
        if not url_accessible(url):
            raise ValueError("Invalid website URL")
        if isStringEmpty(company_name):
            raise ValueError("Invalid or empty System Input") 
        else:
            system_prompt = "You are an assistant that analyzes the contents of several relevant pages from a company website \
                            and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown.\
                            Include details of company culture, customers and careers/jobs if you have the information."
            openai = OpenAI()
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": self.get_brochure_user_prompt(company_name, url)}
                ],
        )
        return response.choices[0].message.content

    def messages_for(self, website:Website, system_prompt:str):
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": self.get_user_prompt_for_summarizer(website)},
        ]


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
    
