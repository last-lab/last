"""
   SOUL API 支持chat功能
"""
import json
from .base_model import HTTPAPILLMModel


class SoulAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://buzz.soulapp.cn/api/v1/chat/completion"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "auth": self.api_key,
            "username": "soul_test",
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

        # resp = requests.post(self.url, headers=self.headers, data=json.dumps(payload))
        _error = None
        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )
        except Exception as e:
            _error = e
        if _error is None:
            return resp
        else:
            return {
                "_error": _error
            }

    def parse(self, response):
        if "_error" in response:
            return (False, response["_error"])
        # print(response)
        return (
            True,
            response["data"]['choices'][0]["text"],
        )
