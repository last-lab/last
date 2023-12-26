"""
   蜜度 Midu API
"""
import json
from .base_model import HTTPAPILLMModel


class MiduAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://www.midu.com/miduwgt/gateway/api/values/question"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "model": "midu-michao",
            "query": messages[-1]["content"],
            **kwargs,
        }
        # len(payload["query"]) < 4096
        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )
            
        except Exception as e:
 
            return e
        return resp

    def parse(self, response):
        if "code" not in response:
            return (False, "Midu Api Error")
        
        if response["code"] != "0000":
            return (False, response["message"])
        
        return (True, response["data"])
