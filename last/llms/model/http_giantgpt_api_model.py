"""
    巨人网络 giantgpt llm api
"""

import json
from .base_model import HTTPAPILLMModel


class GiantgptAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://giantgpt.ztgame.com/api/generate"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "prompt": messages[-1]["content"],
            # **kwargs,
        }

        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )
            
        except Exception as e:
 
            return e

        return resp

    def parse(self, response):
        if "status" not in response:
            return (False, "error")
        else:
            if response['status'] == '1':
                return (False, response['msg'])

        return (
            True,
            response["generate_text"][0],
        )
