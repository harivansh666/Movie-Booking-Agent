from langchain_google_genai import ChatGoogleGenerativeAI
from .settings import get_settings
from functools import lru_cache
@lru_cache(maxsize=1)
def get_llm()-> ChatGoogleGenerativeAI:
    varibles = get_settings()
    return ChatGoogleGenerativeAI(
    model=varibles.model,
    max_tokens=None,
    temperature=varibles.gemini_temprature,
    timeout=60  ,
    max_retries=3,
    )
    