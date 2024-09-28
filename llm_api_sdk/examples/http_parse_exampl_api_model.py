# Copyright © 2023 Shanghai AI lab
# All rights reserved.
"""
This example is intended to demonstrate how to fill the code block of the parse function.
"""
import json
from .base_model import HTTPAPILLMModel


class ParseExamplAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://ParseExampl/chat/api"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "BEAR " + self.api_key,
        }

    async def generate(self, messages, *args, **kwargs):
        formatted_messages = [
            {
                "role": item["role"],
                "content": item["content"],
            }
            for item in messages
        ]
        payload = {
            "messages": formatted_messages,
            **kwargs,
        }
        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )
        except Exception as e:
            return e
        return resp

    def parse(self, response):
        if response is None:
            return (False, "API ERROR!")
        if response["code"] != 0:
            if str(response["code"]).startswith("4001"):
                return (False, "LLM Server ERROR!")
            elif str(response["code"]).startswith("4003"):
                return (False, "Database ERROR!")
            elif str(response["code"]).startswith("30"):
                return (False, "System ERROR!")
            elif str(response["code"]).startswith("20"):
                return (False, "Params ERROR!")
            elif str(response["code"]).startswith("10"):
                return (False, "Key ERROR!")
        return (
            True,
            response["data"]["message"]["content"],
        )
