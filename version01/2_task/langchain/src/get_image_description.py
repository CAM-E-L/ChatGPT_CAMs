import os, openai
import pandas as pd
from langchain.schema import HumanMessage, SystemMessage
from datetime import datetime

from src.initial_prompt import initial_prompt
from src.llm import chat_model
from src.token_counter import count_tokens
from src.encode_image import encode_image

def process_images_directory(directory):

    memory = initial_prompt
    results = []
    
    for image_file in os.listdir(directory):
        if image_file.lower().endswith(('png', 'jpg', 'svg')):
            image_path = os.path.join(directory, image_file)
            encoded_image = encode_image(image_path)
        
            description, memory = get_image_description(encoded_image, memory)           
            results.append([image_file, description])
    
    df = pd.DataFrame(results, columns=['CAM Name', 'Beschreibung'])
    csv_path = os.path.join(directory, f"CAM_Beschreibung_{datetime.now()}.csv")
    df.to_csv(csv_path, index=False)

def get_image_description(encoded_image, memory):

    messages = [
        SystemMessage(content=memory),
        HumanMessage(content=f"{encoded_image}")
    ]

    response = chat_model.invoke(input=messages)
    memory = initial_prompt
    
    return response.content, memory