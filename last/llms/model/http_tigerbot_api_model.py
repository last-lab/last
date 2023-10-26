'''
   Tigerbot API 没有chat功能 仅支持单条数据 
'''
import requests
from .base_model import HTTPAPILLMModel

        
class TigerbotAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://api-bz7ic07j.tigerbot.com/v1/chat/completions"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": 'Bearer ' + self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):

        payload = {
            "model": "tigerbot-70b-chat",
            "query": messages[-1]["content"],
            **kwargs,
        }

        return requests.post(self.url, headers=self.headers, json=payload).json()

    def parse(self, response):

        if "error" in response:
            return(
                False,
                response["error"]["message"]
            )
        
        return (
            True,
            response["result"],
        )


# if __name__ == "__main__":
#     hb = TigerbotAPILLMModel("2dc003e5bd4ad9c66fbf05c4c9afd61922526dcfabe79d7673d66e1e51e901e9")
#     resp = hb.generate(prompt="", messages="印度尼西亚的首都在哪里")

#     print(resp)
#     print(hb.parse(resp))
