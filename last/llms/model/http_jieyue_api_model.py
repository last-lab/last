"""
   Jieyue API WIP
"""
import json
from .base_model import HTTPAPILLMModel


class JieyueAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://b-openapi.basemind.com/openapi/v1/chat/completions"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
            "X-Request-Orgcode": "wxb",
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "model": "open_prod_jy_model",
            "messages": messages,
            **kwargs,
        }
        try:
            
            result = await self.async_post(
                url=self.url, headers=self.headers, data=json.dumps(payload)
            )

            print(result)
        except Exception as e:
            return e
        return result

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
