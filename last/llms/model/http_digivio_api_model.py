"""
    迪智伟奥模型 API
"""
import json
from .base_model import HTTPAPILLMModel


class DigivioAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://chat.digivio.net/api/v1/nlp/completions'
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "messages": messages[-1]["content"],
            "temperature": 0.2,
            "top_p": 0.4,
            "max_token_length": 512,
        }
        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )
            
        except Exception as e:

            return e
        return resp

    def parse(self, response):
        if  "code" not in response or response["code"] != 200:
            return (False, "request error")
        return (True, response["data"])
