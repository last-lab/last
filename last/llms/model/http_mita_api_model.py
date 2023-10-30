'''
   mita API 没有chat功能 仅支持单条数据 
'''
import time
import requests
from .base_model import HTTPAPILLMModel

        
class MitaAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.make_order_url = 'https://xiezuocat.com/html/api/generate/doc'
        self.get_result_url = 'https://xiezuocat.com/html/api/generation/doc/'

        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "secret-key": self.api_key,
        }

    async def make_order(self, content):
        data = {
            "title": content
        }
        response = requests.post(self.make_order_url, json=data, headers=self.headers)
        if response.status_code == 200:
            d = response.json()
            return d['data']['doc_id']
        else:
            
            return int(response.status_code)

    def get_result(self, id):
        response = requests.get(self.get_result_url+id, headers=self.headers)
        status_code = response.status_code
        if status_code == 200:
            d = response.json()
            if d['errCode'] == 0:
                return d['data']['content']
            elif d['errCode'] == 4000 or d['errCode'] == 4001:
                return False
        return None

    async def generate(self, prompt, messages, *args, **kwargs):

        data = {
            "title": messages[-1]["content"]
        }
        response = requests.post(self.make_order_url, json=data, headers=self.headers)
        if response.status_code == 200:
            d = response.json()
            
            return d['data']['doc_id']
        else:
            
            return int(response.status_code)

       

    def parse(self, response):
        if isinstance(response, str):
            while True:

                data = self.get_result(response)
                if data == False:
                    time.sleep(1)
                else:
                    return(
                        True,
                        data
                    ) 
        else:
            return(
                False,
                'make order error:'+str(response)
            ) 
