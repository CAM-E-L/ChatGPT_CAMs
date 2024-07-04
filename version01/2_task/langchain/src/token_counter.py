import tiktoken

def count_tokens(text, model_name="gpt-4o"):
    encoding = tiktoken.encoding_for_model(model_name)
    tokens = encoding.encode(text)
    return len(tokens)