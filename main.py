import os
from dotenv import load_dotenv
from config import Config
from inference import Inference
from find import FindInfo
#from inference import chat, init_rp

def main():
    load_dotenv()
    tavily_key = os.getenv("TAVILY_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")

    if not tavily_key or not groq_key:
        raise EnvironmentError("TAVILY_API_KEY and GROQ_API_KEY must be set in .env")
    
    os.environ["TAVILY_API_KEY"] = tavily_key
    os.environ["GROQ_API_KEY"] = groq_key 

    config = Config()
    user_prompt = input("Prompt: ")
    #rp_prompt = f"{config.wiki_init} \n\n {config.sys_prompt_rp} {config.character} \n"
    # #Inference(sys_prompt=rp_prompt, user_prompt=user_prompt)
    # info_prompt = f"{config.wiki_init} \n {config.sys_prompt_info} \n"
    # print(info_prompt)
    # Inference(sys_prompt=info_prompt, user_prompt=user_prompt)
    #print(info_prompt)
    find = FindInfo(user_prompt=user_prompt, config=config)



if __name__ == "__main__":
    main()