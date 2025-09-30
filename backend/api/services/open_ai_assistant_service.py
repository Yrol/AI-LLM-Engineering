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
            # A special scenario for priming the LLM to exclude items that are not being sold (RAG is another better way of achieving this)
            base_message_template = (
                "We do not sell {item}. If a customer asks about {item}, "
                "politely inform them that {item} are not available."
            )
            
            no_sell_items = ["hat", "hats", "cap", "caps"]

            last_msg = messages[-1] if messages else {}
            last_content = last_msg.get("content", "").lower()

            if last_msg.get("role") == "user":
                for item in no_sell_items:
                    if item in last_content:
                        system_message = f"System note: {base_message_template.format(item=item)}"
                        messages = [{"role": "system", "content": system_message}] + messages
                        break

            # Always prepend the base prompt
            messages = [{"role": "system", "content": prompt}] + messages
            response = self.openai.chat.completions.create(
                model=self.model, 
                messages=messages
            )
            print(response.choices[0].message.content)
            return response.choices[0].message.content