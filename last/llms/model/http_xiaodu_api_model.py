"""
   小度灵机模型 API
"""
import json
from .base_model import HTTPAPILLMModel


class XiaoDuAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'http://dueros-h2-debug.baidu.com/llm/review/exec'
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "text": messages[-1]["content"],
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
        if  "status_code" not in response or response["status_code"] != 200:
            return (False, "request error")
        return (True, response["reply"])
