"""
   达观数据 曹植 API  
"""
import json
from .base_model import HTTPAPILLMModel


class CaozhiAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://cztest-api.datagrand.com/chat"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
        }

    async def generate(self, prompt, messages, *args, **kwargs):

        format_message = [
            {
                "role": item["role"],
                "content": item["content"],
            } for item in messages
        ]
        
        payload = {
            "messages": format_message,
            "max_tokens": kwargs["max_tokens"],
            "top_p": kwargs["top_p"],
        }
        print(payload)

        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )

            
        except Exception as e:
 
            return e
        return resp

    def parse(self, response):
        if response is None:
            return (False, "API ERROR")
        response = json.loads(response)
        return (
            True,
            response["data"][0][0]["text"],
        )
