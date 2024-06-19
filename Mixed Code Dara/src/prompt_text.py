""" 
prompt template
"""

# set language of output
language = "German"

# explain the specific topic of the CAM
specific_topic = """
People had the task of reflecting on their experiences of a newly introduced "open space" office (new office). Thereby two networks side by side were drawn, the left about the past expectations regarding the new office ("damalige Erwartungen ans neue Büro"), the right about the current experiences ("aktuelles Erleben im neuen Büro").
"""

# set a specific task
specific_topic_task = """
Explain the two drawn networks separately and compare them with each other.
"""


# explain data structure of CAMs (picture approach)
prompt = """

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
7) {specific_topic_task}
8) Write in {language}.
>
    Answer: """