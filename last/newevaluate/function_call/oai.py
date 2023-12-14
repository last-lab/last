import openai
def call(key, messages, model='gpt-4'):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        request_timeout=150, 
        temperature = 0,
        api_key = key
    )
    response_message = response["choices"][0]["message"]
    return response_message['content']