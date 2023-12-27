"""
   阅文 YueWriter API 
"""
import json
from .base_model import HTTPAPILLMModel


class YueWriterAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://yai-writer.yuewen.com/api/v1/chat/completions"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "prompt": messages[-1]["content"],
        }
        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )
            
        except Exception as e:
 
            return e
        return resp

    def parse(self, response):
        if "code" not in response:
            return (False, "System Error(回复与文档有差异)")
        if response["code"] != 0:
            if response["code"] == -10001 or response["code"] == -10002:
                return (True, response["msg"])
            return (False, response["msg"])
        return (True, response["data"])
