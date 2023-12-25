# Copyright © 2023 Shanghai AI lab
# All rights reserved.
"""
This example represents the fundamental version.
"""
import json
from .base_model import HTTPAPILLMModel


class FundamentalAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://Fundamental/v1/chat"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }

    async def generate(self, *args, **kwargs):
        payload = {
            "query": "你好",
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
            return (False, response["error"])

        return (
            True,
            response["result"],
        )
