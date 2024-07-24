import os
from dotenv import load_dotenv
import argparse
from langchain_community.tools.tavily_search import TavilySearchResults
from transcription import get_sound, transcribe
from inference import rag_inference

def parse_arguments():
    parser = argparse.ArgumentParser(prog="Voice to Search")
    parser.add_argument("seconds", type=int, default=5, help="Duration of recording to be transcribed")
    return parser.parse_args()

def search_tavily(query):
    search = TavilySearchResults(max_results=2)
    search_results = search.invoke(query)
    return search_results

def main():
    load_dotenv()
    tavily_key = os.getenv("TAVILY_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    if not tavily_key or not groq_key:
        raise EnvironmentError("TAVILY_API_KEY and GROQ_API_KEY must be set in .env")
    
    os.environ["TAVILY_API_KEY"] = tavily_key
    os.environ["GROQ_API_KEY"] = groq_key 

    get_sound()
    transcibed_text = transcribe()
    search_results = search_tavily(transcibed_text)
    print(search_results)

    print(rag_inference())

if __name__ == "__main__":
    args = parse_arguments()
    main()
