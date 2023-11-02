"""
   mita API 没有chat功能 仅支持单条数据 
"""
import json
import time
import aiohttp
from .base_model import HTTPAPILLMModel


class MitaAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_order_url = "https://xiezuocat.com/html/api/generate/doc"
        self.get_result_url = "https://xiezuocat.com/html/api/generation/doc/"

        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "secret-key": self.api_key,
        }

       
    async def async_get(self, url, headers):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                status_code = response.status
                if status_code == 200:
                    d = await response.json()
                if d["errCode"] == 0:
                    return d["data"]["content"]
                elif d["errCode"] == 4000 or d["errCode"] == 4001:
                    return False
            return None

    async def generate(self, prompt, messages, *args, **kwargs):
        data = {"title": messages[-1]["content"]}
        try:
            response = await self.async_post(
                self.make_order_url, headers=self.headers, data=json.dumps(data)
            )
            status_code = 200
        except Exception as e:
            status_code = e
            

        if status_code == 200:
            d = response
            while True:
                data = await self.async_get(
                    url=self.get_result_url + d["data"]["doc_id"],
                    headers=self.headers
                )
                if data == False:
                    time.sleep(0.5)
                else:
                    return data
        else:
            return status_code

    def parse(self, response):
        
        if isinstance(response, str):
            return (True, response)
        else:
            return(
                False,
                'make order error: %s' % str(response),
            ) 

