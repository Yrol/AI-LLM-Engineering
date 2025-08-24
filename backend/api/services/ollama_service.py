import requests
from openai import OpenAI
import json
from ..helper.validators import  url_accessible, isStringEmpty
from ..helper.website import Website
from ..helper.constants import Method

class OllamaService:
    
    def __init__(self):
        self.endpoint = "http://ollama:11434/api/chat"
        
    
    def request_validator(self, model, messages, stream):
        
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

    def ollama_ask_anything(self, model, messages, stream, raw_data, method):
        
        self.request_validator(model, messages, stream)
            
        if  method == Method.OPENAI.value: # making a call to Ollama through OpenAI by poiting to the ollama running in Docker
            ollama_via_openai = OpenAI(base_url='http://ollama:11434/v1', api_key='ollama')
            response = ollama_via_openai.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.json()
        else: # making a call to Ollama running in Docker
            response = requests.post(self.endpoint, json=raw_data)
            return response.json()
        
        
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
        user_prompt += (
            "please decide which of these are relevant web links for a brochure about the company, respond with the full https URL in JSON format. "
            "Do not include Terms of Service, Privacy, email links.\n"
            "Links (some might be relative links):\n"
        )
        user_prompt += "\n".join(website.links)
        return user_prompt
    
    def get_links(self, url:str):
        website = Website(url)  # Assumes Website(url).links and .url work as before
        system_prompt = self.get_system_prompt_for_brochure()
        user_prompt = self.get_links_user_prompt(website)
        
        ollama_via_openai = OpenAI(base_url='http://ollama:11434/v1', api_key='ollama')
        response = ollama_via_openai.chat.completions.create(
            model="mistral",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        print(response.json)
        
        return response.json()
    
    def get_all_details(self, url: str):
        result = "Landing page:\n"
        result += Website(url).get_contents()
        links_response = self.get_links(url)

        if isinstance(links_response, str):
            links_response = json.loads(links_response)

        content_str = links_response['choices'][0]['message']['content'].strip()
        links_dict = json.loads(content_str)

        print("Found links:", links_dict)
        for link in links_dict["links"]:
            link_url = link["url"].strip()
            # Only fetch contents for http(s) URLs
            if link_url.lower().startswith("http://") or link_url.lower().startswith("https://"):
                result += f"\n\n{link['type']}\n"
                result += Website(link_url).get_contents()
            else:
                print(f"Skipping non-HTTP(S) URL: {link_url}")

        return result
    
    def get_brochure_user_prompt(self, company_name:str, url:str):
        user_prompt = f"You are looking at a company called: {company_name}\n"
        user_prompt += f"Here are the contents of its landing page and other relevant pages; use this information to build a short brochure of the company in markdown.\n"
        user_prompt += self.get_all_details(url)
        user_prompt = user_prompt[:5_000] # Truncate if more than 5,000 characters
        return user_prompt
    
    def ollama_create_brochure(self, company_name:str, url:str):
        if not url_accessible(url):
            raise ValueError("Invalid website URL:" + url)
        if isStringEmpty(company_name):
            raise ValueError("Invalid or empty System Input")
        
        system_prompt = (
            "You are an assistant that analyzes the contents of several relevant pages from a company website "
            "and creates a short brochure about the company for prospective customers, investors and recruits. Respond in markdown. "
            "Include details of company culture, customers and careers/jobs if you have the information."
        )
        user_prompt = self.get_brochure_user_prompt(company_name, url)
        
        payload = {
            "model": "mistral",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False
        }
        response = requests.post(self.endpoint, json=payload)
        return response.json()["message"]["content"]

        
    # def ollama_web_summerizer(self):
        
    #     website = Website("https://www.bbc.com")
    #     main_text = website.text
    #     payload = {
    #         "model": "tinyllama",
    #         "messages": [
    #             {
    #                 "role": "system",
    #                 "content": "You are an assistant that analyzes the contents of a website and provides a short summary, ignoring text that might be navigation related. Respond in markdown."
    #             },
    #             {
    #                 "role": "user",
    #                 "content": main_text
    #             }
    #         ],
    #         "stream": False
    #     }
        
    #     response = requests.post(self.endpoint, json=payload)
    #     return response.json()
        
        
        
        
        
        