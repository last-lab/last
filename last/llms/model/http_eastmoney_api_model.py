"""
   东方财富奇思妙想金融大模型 API 
"""
import json
from .base_model import HTTPAPILLMModel


class EastMoneyAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://llm-platform.eastmoney.com/api/verify/ask2"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
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
            "messages": formatted_messages,
            "token": self.api_key,
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
        if response["code"] == -7 and "message" in response:
            return (
                True,
                response["message"],
            )
        elif response["code"] == 0 :
            return (
                True,
                response["data"],
            )
        else:
            return (False, "Api Error!")
