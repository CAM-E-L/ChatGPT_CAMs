from langchain_openai import ChatOpenAI
from src.API_Key import OpenAI_API_KEY

chat_model = ChatOpenAI(model='gpt-4o', openai_api_key= OpenAI_API_KEY, max_tokens=500)
