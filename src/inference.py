import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain import hub

def rag_inference(context: str = None, query: str = None, model: str = "llama3-8b-8192"):
    model = ChatGroq(model=model)
    prompt = hub.pull("rlm/rag-prompt")

    if query is None:
        raise ValueError("'query' parameter is None, please set it to a string")

    prompt_applied = prompt.invoke(
        {"context": context, "question": query}
    ).to_messages()

    output = model.invoke(prompt_applied)

    return output
