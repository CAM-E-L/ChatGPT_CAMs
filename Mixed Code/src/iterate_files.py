import os
from src.encode_image import encode_image
import requests
from src.headers import headers

def iterate_files(directory_path):
    for filename in os.listdir(directory_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            image_path = os.path.join(directory_path, filename)
            
            # Encode the image
            base64_image = encode_image(image_path)

            # Prepare the payload
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "You are a helpful assistant. Describe what you can see in this image, paying attention to key concepts and relationship between them. In the end provide a summary of what you have seen"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }

            # Send the request to the OpenAI API
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            description = response.json()['choices'][0]['message']['content']

            # Print the response
            print(f"Response for {filename}:")
            # print(f"Response:")
            print(description)
            print("\n" + "="*50 + "\n")