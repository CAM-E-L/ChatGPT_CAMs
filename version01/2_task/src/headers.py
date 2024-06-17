from src.API_key import openai_api_key

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {openai_api_key}"
}