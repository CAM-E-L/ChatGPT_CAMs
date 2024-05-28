import os

# from langchain.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAI
from langchain.callbacks import get_openai_callback

from langchain.callbacks import get_openai_callback
from langchain import PromptTemplate, LLMChain
import pandas as pd
import random
import itertools
import time
from collections import defaultdict
import tiktoken
import numpy as np


""" 
cost estimation
"""


def generate_custom_pattern(pattern_text, repeat_count):
    # Generate the repeated pattern by repeating the entire `pattern_text`
    # `repeat_count` times, separating each repetition with a newline character
    result = (pattern_text + "\n") * repeat_count

    return result.rstrip()


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def estimate_cost(string_in: str, string_out: str, model_name: str) -> float:
    """Estimate the cost of using GPT-4 or GPT-3.5 (turbo) based on the number of tokens."""
    pricing = {
        "gpt-4": {"input": 30.00 / 1e6, "output": 60.00 / 1e6},
        "gpt-3.5-turbo-0125": {"input": 0.50 / 1e6, "output": 1.50 / 1e6},
    }
    num_tokens_in = len(tiktoken.get_encoding("cl100k_base").encode(string_in))
    num_tokens_out = len(tiktoken.get_encoding("cl100k_base").encode(string_out))

    if model_name in pricing:
        cost_input = num_tokens_in * pricing[model_name]["input"]
        cost_output = num_tokens_out * pricing[model_name]["output"]
        total_cost = cost_input + cost_output
        return num_tokens_in, cost_input, cost_output, total_cost
    else:
        raise ValueError("Unsupported model name")


def print_cost_report(
    gpt4_input, gpt4_output, gpt4_costs, gpt35_input, gpt35_output, gpt35_costs, n_calls
):
    gpt4_total_anchor_cost = gpt4_costs * n_calls
    gpt35_total_anchor_cost = gpt35_costs * n_calls

    report = f"""
Cost Estimation Report:

GPT-4:
- Input Tokens Cost: {gpt4_input:,.5f} USD
- Output Tokens Cost: {gpt4_output:,.5f} USD
- Total Cost for Single API-Call: {gpt4_costs:,.5f} USD
- Total Cost for {n_calls} API-Calls: {gpt4_total_anchor_cost:,.5f} USD

GPT-3.5 Turbo:
- Input Tokens Cost: {gpt35_input:,.5f} USD
- Output Tokens Cost: {gpt35_output:,.5f} USD
- Total Cost for Single API-Call: {gpt35_costs:,.5f} USD
- Total Cost for {n_calls} API-Calls: {gpt35_total_anchor_cost:,.5f} USD
"""
    print(report)


""" 
Prompt-Template
"""


def prompt_template(
    df,
    chosen_partitions,
    template,
    model_name="gpt-4",
    max_permutations=5,
    iterations_before_pause=10,
    pause_duration_seconds=15,
    seconds_to_sleep_each_loop=0.001,
):

    filtered_df = df[df["partition"].isin(chosen_partitions)]
    # words_list = filtered_df["words"].tolist()
    words_list = ", ".join(filtered_df["words"].tolist())

    prompt = PromptTemplate(template=template, input_variables=["items_list"])
    number_of_run = 0

    prompt_text = prompt.format(
        items_list=words_list,  # Use the filtered words list
    )

    return prompt_text


""" 
API-Call
"""


def basic_API_call(
    openai_api_key,
    words_list,
    template,
    input_variables=[
        "items_list",
    ],
    model_name="gpt-4",
    max_tokens=150,
):

    prompt = PromptTemplate(template=template, input_variables=input_variables)
    # top_p_value = float("0")
    seed = 123
    llm_chain = LLMChain(
        prompt=prompt,
        llm=ChatOpenAI(
            # llm=OpenAI(
            temperature=0.0,
            openai_api_key=openai_api_key,
            model_name=model_name,
            max_tokens=max_tokens,
            # model_kwargs={"top_p": top_p_value, "seed": seed},
            model_kwargs={"seed": seed},
        ),
        return_final_only=False,
    )

    with get_openai_callback() as cb:
        response = llm_chain.invoke(
            {
                "items_list": words_list,
            }
        )
        print(cb)

    return response


def process_partitions(
    df,
    prompt_text,
    openai_api_key,
    model,
    chosen_partitions=None,
    max_tokens=150,
    max_API_calls=2,
    wait_seconds=10,
):
    results = []
    response_full = []
    batches_processed = 0

    # Generate all combinations of partitions if no specific partitions are provided
    if chosen_partitions is None:
        unique_partitions = df["partition"].unique()
        all_combinations = list(itertools.combinations(unique_partitions, 2))
        chosen_partitions = all_combinations
    else:
        chosen_partitions = chosen_partitions

    # Process each set of partitions
    for partitions in chosen_partitions:
        filtered_df = df[df["partition"].isin(partitions)]
        words_list = ", ".join(filtered_df["words"].tolist())

        response = basic_API_call(
            openai_api_key=openai_api_key,
            words_list=words_list,
            template=prompt_text,
            input_variables=[
                "items_list",
            ],
            model_name=model,
            max_tokens=max_tokens,
        )
        results.append(response["text"])
        response_full.append(response)

        time.sleep(wait_seconds)

        batches_processed += 1
        if batches_processed >= max_API_calls:
            break

    return results, response_full
