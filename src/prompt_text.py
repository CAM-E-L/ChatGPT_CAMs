""" 
prompt template
"""

test_prompt_text = """
A person is asked to describe a situation based on a few words:
"""

desired_ouput_neg = """
Dave Smith is developing an advertisement for a new housing development his firm is about to start. 
The development is located in a low area which has flooded in the past. 
The company has recently done some work to reduce the danger of flooding in the future. 
In the preliminary advertisement, Smith has included a statement indicating that the firm has solved the flooding problem. 
The fact is that if a flood occurs, the homes are still likely to have up to a foot of water standing in the yards.
"""

desired_ouput_pos = """
Dave Smith is developing an advertisement for a new housing development his firm is launching soon. 
Located in an area prone to flooding in the past, the company has undertaken significant improvements to mitigate this risk. 
In the preliminary advertisement, Smith highlights the firm's commitment to enhancing flood defenses. 
While acknowledging that extreme weather could still bring water into the yards, the firm has effectively minimized the potential 
for home damage, ensuring the development is safer and more resilient than ever before.
"""

task = """
"Imagine a scenario where a construction company is developing a new housing complex using a revolutionary but untested material system. 
The material is known to be 'wartungsintensiv' (maintenance-intensive), has an uncertain 'Akzeptanz eines neuen Materialsystems' 
(acceptance of a new material system), and is 'leicht zerstörbar' (easily destructible). 

Write a short story related to this new material system.
Imagine you are 'Dave Smith', a marketing manager at the construction company.
"""


template_partitions = """
<Background:

<Task:
"Imagine a scenario where a construction company is developing a new housing complex using a revolutionary but untested material system. 
The material is known to be 'wartungsintensiv' (maintenance-intensive), has an uncertain 'Akzeptanz eines neuen Materialsystems' 
(acceptance of a new material system), and is 'leicht zerstörbar' (easily destructible). 

Write a short story related to this new material system.
Imagine you are 'Dave Smith', a marketing manager at the construction company.
({items_list})>
    Answer: """
