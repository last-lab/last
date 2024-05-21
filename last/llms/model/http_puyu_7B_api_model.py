import json
import requests
from .base_model import HTTPAPILLMModel
from openai import OpenAI

import logging

class Puyu7BAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://180.184.173.40:22491/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        formatted_messages = [
            {
                "role": item["role"],
                "content": item["content"],
            }
            for item in messages
        ]
        payload = {
            "model": "internlm2-chat", 
            "messages": formatted_messages,
            "max_tokens": 1024, "top_k": 40,
            "temperature": 1.0, "top_p": 0.8, "repetition_penalty": 1.01,
        }

        try:
            response = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )
        except Exception as e:
            return e

        return response

    def parse(self, response):
        if "success" not in response and "code" not in response:
            return (
                True,
                response["choices"][0]["message"]["content"],
            )
        else:
            return(
                False,
                response["msg"]
            )
