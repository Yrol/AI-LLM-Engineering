from ..helper.validators import check_open_ai
from openai import OpenAI
import json

class OpenAiTicketingAssistantService:
    '''
    There's a particular dictionary structure that's required to describe our function.
    In this case we're adding the function get_ticket_price to be used as a tool.
    '''
    
    price_function = {
        "name": "get_ticket_price",
        "description": "Get the price of a return ticket to the destination city. Call this whenever you need to know the ticket price, for example when a customer asks 'How much is a ticket to this city'",
        "parameters": {
            "type": "object",
            "properties": {
                "destination_city": {
                    "type": "string",
                    "description": "The city that the customer wants to travel to",
                },
            },
            "required": ["destination_city"],
            "additionalProperties": False
        }
    }
    
    ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}
    
    tools = [{"type": "function", "function": price_function}]
    
    def __init__(self):
        self.api_key_response = check_open_ai("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"
        self.openai = OpenAI()
    
    def open_ai_ticketing_assistant(self, messages:str, prompt:str):
        
        if isinstance(self.api_key_response, str):
            raise ValueError(self.api_key_response)
        else:
            # Always prepend the base prompt
            messages = [{"role": "system", "content": prompt}] + messages
            response = self.openai.chat.completions.create(
                model=self.model, 
                messages=messages,
                tools=self.tools
            )
            
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                response, city = self.handle_tool_call(message)
                messages.append(message)
                messages.append(response)
                response = self.openai.chat.completions.create(model=self.model, messages=messages)
                
            print(response.choices[0].message.content)
            return response.choices[0].message.content
        
    def get_ticket_price(self, destination_city):
        print(f"Tool get_ticket_price called for {destination_city}")
        city = destination_city.lower()
        return self.ticket_prices.get(city, "Unknown")
    
    '''
    Function for unpacking which tool to be used, but in this case there will be only one tool available
    '''
    def handle_tool_call(self, message):
        tool_call = message.tool_calls[0]
        print(tool_call)
        arguments = json.loads(tool_call.function.arguments)
        city = arguments.get('destination_city')
        price = self.get_ticket_price(city)
        
        '''
        Role - tool (similar to user, assistant & etc)
        tool_call_id - adding an id to the message where it links the message in the correct place (i.e. the order)
        '''
        response = {
            "role": "tool",
            "content": json.dumps({"destination_city": city,"price": price}),
            "tool_call_id": tool_call.id
        }
        return response, city
    