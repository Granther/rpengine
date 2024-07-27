import os
from tavily import TavilyClient
from groq import Groq

class Inference:
    def __init__(self, character_prompt: str = None, config = None):
        self.char_prompt = character_prompt
        self.char_data = self.init_search()
        self.config = config
        self.rp_prompt = self.config.sys_prompt_rp 

    # Perform original data scrape for RP prompt
    def init_search(self):
        self.client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

        char_prompt_eng = f"Tell me about {self.char_prompt}, in detail and depth"
        char_data = self.client.qna_search(char_prompt_eng, search_depth="advance", topic="general")

        return char_data
    
    def generic_search(self, search: str = None):
        response = self.client.qna_search(search, search_depth="basic", topic="general")
        return response
    
    def update_sys_prompt(self, user_prompt: str = None):
        self.char_data += "\n" + self.generic_search(user_prompt)
        self.sys_prompt = self.char_data + "\n\n" + self.rp_prompt
        print(self.sys_prompt)
    
    # Generic inference, gotta handle sys prompt on the backend 
    def infer(self, user_prompt: str = None, model_name: str = "gemma2-9b-it"):
        self.update_sys_prompt(user_prompt)

        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": self.sys_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            model=model_name,
        )

        return chat_completion.choices[0].message.content
