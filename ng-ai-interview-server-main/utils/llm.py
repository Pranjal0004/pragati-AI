import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_model(model: str = "gpt-4o", tools: list = None, temperature: float = 0.5) -> ChatOpenAI:
    api_key = os.getenv("OPENAI_API_KEY", "any")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    model = ChatOpenAI(
        model=model, 
        base_url=base_url,
        api_key=api_key,
        temperature=temperature
    )
    
    if tools and len(tools) > 0:
        model = model.bind_tools(tools)
    return model
