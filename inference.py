import os
from tavily import TavilyClient
from groq import Groq

from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

class Inference:
    def __init__(self, character_prompt: str = None, config = None):
        self.char_prompt = character_prompt
        self.char_data = self.init_search()
        self.config = config
        self.rp_prompt = self.config.sys_prompt_rp 
        self.store = {}
        self.config = {"configurable": {"session_id": "abc2"}}

    # Perform original data scrape for RP prompt
    def init_search(self):
        self.client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

        char_prompt_eng = f"Tell me about {self.char_prompt}, in detail and depth"
        char_data = self.client.qna_search(char_prompt_eng, search_depth="advance", topic="general")

        return char_data
    
    def generic_search(self, search: str = None):
        response = self.client.qna_search(search, search_depth="basic", topic="general")
        return response
    
    def add_ctx(self, search: str):
        prompt = self.char_data + "\n\n" + "Rephrase the below question to be about the above context."
        response = self.infer(sys_prompt=prompt, user_prompt=search)
        return response

    def update_sys_prompt(self, user_prompt: str = None):
        self.char_data += "\n" + self.generic_search(self.add_ctx(user_prompt))
        self.sys_prompt = self.char_data + "\n\n" + self.rp_prompt
    
    # Generic inference, gotta handle sys prompt on the backend 
    # def user_infer(self, user_prompt: str = None, model_name: str = "gemma2-9b-it"):
    #     self.update_sys_prompt(user_prompt)

    #     print(self.sys_prompt)

    #     client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    #     chat_completion = client.chat.completions.create(
    #         messages=[
    #             {
    #                 "role": "system",
    #                 "content": self.sys_prompt
    #             },
    #             {
    #                 "role": "user",
    #                 "content": user_prompt
    #             }
    #         ],
    #         model=model_name,
    #     )

    #     return chat_completion.choices[0].message.content

    def infer(self, user_prompt: str = None, sys_prompt: str = None, model_name: str = "gemma2-9b-it"):
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": sys_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            model=model_name,
        )

        return chat_completion.choices[0].message.content

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]

    def user_infer(self, user_prompt: str = None, model_name: str = "gemma2-9b-it"):
        self.update_sys_prompt(user_prompt)
        print(self.sys_prompt)

        model = ChatGroq(model=model_name)
        with_message_history = RunnableWithMessageHistory(model, self.get_session_history)

        response = with_message_history.invoke(
            [
                HumanMessage(content=user_prompt), 
                SystemMessage(content=self.sys_prompt)
            ],
            config=self.config,
        )

        return response.content