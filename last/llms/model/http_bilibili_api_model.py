"""
   bilibili API 没有chat功能 仅支持单条数据 
   按照时间有次数限制
"""
import json
from .base_model import HTTPAPILLMModel


class BilibiliAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://api.bilibili.com/x/ai/chat/openapi/v1/chat/index70"
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
            "access_key": self.api_key,
            "messages": formatted_messages,
            **kwargs,
        }
        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload, ensure_ascii=False).encode('utf-8')
            )

        except Exception as e:

            return e
        return resp

    def parse(self, response):
        if "status" not in response or response["status"] != 0:
            return (False, response["msg"])

        return (
            True,
            response["data"]["result"]["content"],
        )
