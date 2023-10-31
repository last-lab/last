'''
   Wuya API 没有chat功能 仅支持单条数据 
'''
import requests
from .base_model import HTTPAPILLMModel

        
class WuyaAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key="", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://223.166.177.4:8091/chat/wuya"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            # "Authorization": self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):

        payload = {
            "query": messages[0]["content"],
            "query_intention": "knowledge"
        }


        return requests.post(self.url, headers=self.headers, json=payload).json()

    def parse(self, response):

        try:
            answer = response['wuya_output']
            return (
                True,
                answer,
            )
        except Exception as e:
            answer = None

            return (
                False,
                e
            )


