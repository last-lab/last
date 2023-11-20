"""
    无限光年 光语慧言 API 
"""
import json
from .base_model import HTTPAPILLMModel


class InfchatAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://api.infly.cn/chat/api/v2/send"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            'Authorization': 'APPCODE ' + self.api_key,
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
            "model": "inf-chat",
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
        if response is None:
            return (False, "API ERROR!")

        return (
            True,
            response['data']['choices'][0]['message']['content'],
        )
