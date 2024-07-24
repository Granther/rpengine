import os
from inference import Inference
from config import Config
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults

class FindInfo:
    def __init__(self, sys_prompt: str = None, user_prompt: str = None, model_name: str = "llama3-8b-8192", config = None):
        self.model = ChatGroq(model=model_name)
        self.user_prompt = user_prompt
        self.sys_prompt = sys_prompt 
        self.config = config

        self.should_search()

    def should_search(self):
        # Ask model if the Wiki contains relavant information to answer query
        # If no, continue to search
        # If yes, return to main RP
        eng = "Given the above wiki, simply, does the wiki have enough information to fully answer the below query? Yes or No"
        sys_prompt_eng = f"{self.config.wiki_init}\n{eng}"
        print(sys_prompt_eng)
        inf = Inference(sys_prompt=sys_prompt_eng, user_prompt=self.user_prompt)
        response = inf.infer()

        print(response)

        if "No" or "no" or "NO" in response:
            print("Must search")
        elif "Yes" or "yes" or "YES" in response:
            print("No need to search")

    def search_tavily(query):
        search = TavilySearchResults(max_results=2)
        search_results = search.invoke(query)
        return search_results

if __name__ == "__main__":
    pass



