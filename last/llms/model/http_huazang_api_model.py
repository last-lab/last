"""
   华藏大模型同步问答API
"""

import json
from .base_model import HTTPAPILLMModel


class HuazhangAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://huazang.xiaoi.com/integrationapi/answer/ask-test"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Lang": "zh-cn",
            "Authorization": self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        formatted_messages = [
            {
                "role": item["role"],
                "text": item["content"],
            }
            for item in messages
        ]
        payload = {
            "messages": formatted_messages,
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
        if response["status_code"] != 200:
            return (False, response["reply"])

        return (
            True,
            response["reply"],
        )
