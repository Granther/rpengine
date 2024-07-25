import os
from langchain_groq import ChatGroq
from groq import Groq
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
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

# from langchain_core.chat_history import (
#     BaseChatMessageHistory,
#     InMemoryChatMessageHistory,
# )
# from langchain_core.runnables.history import RunnableWithMessageHistory

# store = {}

# model = ChatGroq(model=model)

# def get_session_history(session_id: str) -> BaseChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = InMemoryChatMessageHistory()
#     return store[session_id]


# with_message_history = RunnableWithMessageHistory(model, get_session_history)

class Inference:
    def __init__(self):
        pass

    def infer(self, sys_prompt: str = None, user_prompt: str = None, model_name: str = "gemma2-9b-it"):
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
