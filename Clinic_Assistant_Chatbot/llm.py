from langchain_groq import ChatGroq
from config import GROQ_API_KEY


def get_llm():
    return ChatGroq(model="qwen/qwen3-32b",
                    api_key=GROQ_API_KEY,
                    temperature=0.1)
