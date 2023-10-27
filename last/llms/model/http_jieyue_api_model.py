'''
   Jieyue API WIP
'''
import requests
from .base_model import HTTPAPILLMModel

        
class JieyueAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://b-openapi.basemind.com/openapi/v1/chat/completions"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": 'Bearer ' + self.api_key,
            "X-Request-Orgcode": "wxb"
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        try:

            payload = {
                "model": "open_prod_jy_model",
                "messages": messages,
                **kwargs,
            }

            return requests.post(self.url, headers=self.headers, json=payload).json()
        except Exception as e:
            return e

    def parse(self, response):
        if isinstance(response, Exception):
            return (
                False,
                response,
            )
        return (
            True,
            response["choices"][0]["message"]["content"],
        )
