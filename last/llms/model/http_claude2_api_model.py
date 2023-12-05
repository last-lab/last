"""
   claude-2 API 支持中英双语
"""
import json
from .base_model import HTTPAPILLMModel


class Claude2APILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://oneapi.run.place/v1/chat/completions"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }
        self.qps = 2

    async def generate(self, prompt, messages, *args, **kwargs):
        
        formatted_messages = [
            {
                "role": item["role"],
                "content": item["content"],
            }
            for item in messages
        ]
        
        
        payload = {
            "model": "claude-2",
            "messages": formatted_messages,
            "stream": False,
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
        if "error" in response:
            return (False, response["error"]["message"])

        return (
            True,
            response["choices"][0]["message"]["content"],
        )
