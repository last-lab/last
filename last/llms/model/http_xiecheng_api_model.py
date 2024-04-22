"""
   携程问道模型 API
"""
import json
from .base_model import HTTPAPILLMModel


class XieChengAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://wendao3.ctrip.com/chat'
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "query": messages[-1]["content"],
            "restart": "true",
        }
        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )
            
        except Exception as e:

            return e
        return resp

    def parse(self, response):
        response = json.loads(response)
        if  "result" not in response:
            return (False, "request error")
        return (True, json.loads(response["result"])["response"])
