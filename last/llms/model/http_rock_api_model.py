# import requests

# url = "https://kb.rockai.net/open/api/dialogue/v1/syncChat"
# headers = {
#     "Content-Type": "application/json",
#    "Authorization": "Bearer bFzHxDKI6FNbrCtFqLEmBLfKMg3Qff9M"
# }
# data = {
#     "prompt": "你好",
#     "appId": 51
# }
# response = requests.post(url, headers=headers, json=data)
# print(response.json())


"""
   RockAI API 
"""
import json
from .base_model import HTTPAPILLMModel


class RockAIAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://kb.rockai.net/open/api/dialogue/v1/syncChat"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "prompt": messages[-1]["content"],
            "appId": 51
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
        if response["code"] != 200:
            return (True, response["message"])
        return (True, response["data"]["reply"])
