"""
   metaso模型 API
"""
import json
from .base_model import HTTPAPILLMModel


class MetasoAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://metaso.cn/api/search/super'
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "secret-key": self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "question": messages[-1]["content"],
        }
        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )
            
        except Exception as e:

            return e
        return resp

    def parse(self, response):
        # response = json.loads(response)
        d = response
        if  d['errCode'] == 500:
            return (False, d['errMsg'])
        elif d["errCode"] == 404:
            res = "未搜索到结果"
        elif d["errCode"] == 4009:
            res = "领域不支持而拒答"
        else:
            res = d["data"]["answer"]
        return (True, res)
