"""
   Wind Alice API 
"""
import json
from .base_model import HTTPAPILLMModel


class WindAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://m.wind.com.cn/unitedweb/JWindSearch/dynamic/api/aliceChat"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "wind.sessionid": self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "model": "AliceChat",
            "content": messages[-1]["content"],
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
        if isinstance(response, str):
            return (False, "访问出错")

        if response["status"] != "0":
            if response["status"] == "3":
                return (True, response['message'])
            return (False, response['message'])
        
        return (True, response["text"])
