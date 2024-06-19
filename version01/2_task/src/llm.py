from langchain import PromptTemplate, LLMChain
from langchain_openai import ChatOpenAI
import src.API_key as key


llm = ChatOpenAI(model='gpt-4o', openai_api_key=key.openai_api_key, max_tokens=500)

prompt_template = PromptTemplate(template="{initial_prompt}\n\nImage: {image_base64}", input_variables=["initial_prompt", "image_base64"])
chain = LLMChain(prompt=prompt_template, llm=llm)
