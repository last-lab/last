"""
   大智慧惠问 xiaohui API
"""
import json
from .base_model import HTTPAPILLMModel


class XiaohuiAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://xiaohuiapi1.dzh.com.cn/xiaohui/answer"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "token": self.api_key,
            "q": messages[-1]["content"],
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
        if 'status' not in response:
            return (False, "System Error")
        if "error" in response:
            return (False, "API Error")

        return (
            True,
            response["data"],
        )
