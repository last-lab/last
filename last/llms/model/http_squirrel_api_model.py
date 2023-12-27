"""
   松鼠AI API 流数据且只能测某一道题的回答
"""

import hashlib
import re
import time
import random
import json
from .base_model import HTTPAPILLMModel


def get_md5(params: dict, secret: str):
    sorted_keys = sorted(params.keys())
    sorted_dict = {}

    for key in sorted_keys:
        sorted_dict[key] = params[key]
    paramsList = []
    for k, v in sorted_dict.items():
        paramsList.append(k + '=' + str(v))
    paramsStr = '&'.join(paramsList)

    strs = paramsStr + secret
    return get_md5_str(strs)

def get_md5_str(src: str):
    h = hashlib.md5()
    h.update(src.encode(encoding='utf-8'))
    return h.hexdigest()


def get_random_number(array):
    return random.choice(array)


class SquirrelAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://sapi.classba.cn/llmserviceapi/analysis/streamAnalysis"

        params = json.loads(api_key)

        self.app_id = params["app_id"]
        self.course_id = params["course_id"]
        self.question_id = params["question_id"]
        self.seretKey = params["seretKey"]
        
        randArr = ['a', 'b', 'c', 'd', 'e', 'f', 'g',
                'h', 'i', 'j', 'k', 'l', 'm', 'n',
                'o', 'p', 'q', 'i', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z']
        

        self.rand = ""
        i = 0
        while i < 4:
            r = get_random_number(randArr)
            self.rand = self.rand + r
            i += 1
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def add_sign(self, messages):
        secretMp = {
            "course_id": self.course_id,
            "question_id": self.question_id,
            "user_answer": messages[-1]["content"],
            "timestamp": int(time.time()),
            "rand": self.rand,
            "app_id": self.app_id
        }
    
        sign = get_md5(secretMp, self.seretKey)
        secretMp["sign"] = sign
        return secretMp


    async def generate(self, prompt, messages, *args, **kwargs):

        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=self.add_sign(messages), _is_stream=True
            )
            
        except Exception as e:
 
            return e
        return resp

    def parse(self, response):
        # print(response)
        try:
            d = json.loads(response)

            return (False, d["msg"].encode('utf-8').decode('unicode-escape'))
        except Exception as e:
            p = re.compile('data:{"chunk":"(.*?)"}')

            data_list = re.findall(p, response)

            decoded_str_list = [s.encode('utf-8').decode('unicode-escape') for s in data_list]

            return (True, "".join(decoded_str_list))
