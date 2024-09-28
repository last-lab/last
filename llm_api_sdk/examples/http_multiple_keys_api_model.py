# Copyright © 2023 Shanghai AI lab
# All rights reserved.
"""
This example is intended to demonstrate how to fill the code block of
the __init__() function when multiple keys are required (e.g., ak: 'xxx',
sk: 'xxx').
"""
import json
from .base_model import HTTPAPILLMModel


def encode_token(ak, sk):
    token = ak + sk
    return token


class MultipleKeysAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://MultipleKeys/chat/api"
        param = json.loads(api_key)
        ak = param["ak"]
        sk = param["sk"]
        self.token = encode_token(ak, sk)
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.token,
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
        if "error" in response:
            return (False, response["error"]["message"])

        return (
            True,
            response["data"]["message"],
        )
