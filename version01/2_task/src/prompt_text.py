""" 
prompt template
"""
### DEFAULTS:
# set language of output
language = "English"

# explain the specific topic of the CAM (needed)
specific_topic = None

# set a specific task (optional)
specific_topic_task = None


# explain data structure of CAMs (picture approach)
def get_prompt(language, specific_topic, specific_topic_task):
    if specific_topic is None:
        raise ValueError("specific_topic cannot be None")
    
    task_text = f"8) {specific_topic_task}" if specific_topic_task else ""
    return f"""

<Data Structure:
In the picture you see a so called "Cognitive-Affective Map" (CAM), whereby a CAM can be considered as a specific form of mind map drawn by a person regarding a specific topic. There a different elements in the CAM, which you should consider: 
1) There a concepts (also called nodes), which are linked by connections (also called edges).
2) Concepts incorporate an emotional evaluation by representing whether a person associates positive (green stroke), negative (red stroke), neutral (yellow stroke) or ambivalent (purple stroke) emotions with a drawn concept.
2a) Depending on the stroke width of the positive or negative concepts the concept is emotionally evaluated as more positive or negative.
3)  Furthermore, it is possible to specify the connections in different strengths and in two different forms: 
3a) Depending on the width of the line the association between two drawn concepts is stronger.
3b) Solid lines stand for supporting connections and dashed lines stand for inhibitory connections.>

<Specific Topic:
{specific_topic}>

<Task:
1) Write a text no longer than 300 words describing the CAM, consider thereby the specific topic.
2) Write neutrally in the third person.
3) Start with a short introductory sentence that describes the topic.
4) Do not explain the data structure of CAMs.
5) Focus on the drawn concepts and not on the drawn connections.
6) At the end provide a summary paragraph of the drawn CAM.
7) Write in {language}.
{task_text}
>

    Answer: """