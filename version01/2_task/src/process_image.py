
import os
from src.encode_image import encode_image_to_base64
# from src.initial_prompt import initial_prompt
from src.llm import chain

def process_images(directory, prompt):
    descriptions = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".svg"):
            image_path = os.path.join(directory, filename)
            image_base64 = encode_image_to_base64(image_path)
            response = chain.run(initial_prompt=prompt, image_base64=image_base64)
            descriptions.append({"filename": filename, "description": response})

        # In most cases, due to the differences in how PNG and SVG handle image data,
        #  a PNG file will result in a larger Base64-encoded string compared to an SVG file of 
        # the same visual content. SVG’s text-based and scalable nature generally leads to smaller 
        # initial file sizes and therefore smaller Base64-encoded sizes.
    
    # print(descriptions)
    return descriptions   