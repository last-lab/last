"""
   KKBot API
"""
import re
import json
import requests
from .base_model import HTTPAPILLMModel
import random
import time

class KKbotAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 我打算不改变现有格式 api_key userId appId sessionId 都是到这里才被解析出来 延迟处理这些信息

        param = json.loads(api_key)
        self.api_key = param["api_key"]
        self.userId = param["userId"]
        self.appId = param["appId"]
        self.sessionId = param["sessionId"] if "sessionId" in param else "tests"
        self.url = "https://kkbot-llm-saas.emotibot.com/chatService/chat/api/v1/chat/stream/release/{userId}?apiKey={apiKey}".format(
            userId=self.userId, apiKey=self.api_key
        )
        self.clear_url = "https://kkbot-llm-saas.emotibot.com/chatService/chat/api/v1/chat/clear/{userId}".format(
            userId=self.userId
        )
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        
        # payload = json.dumps(
        #     {
        #         "type": "clear",
        #         "data": {"sessionId": self.sessionId, "appId": self.appId},
        #     }
        # )
        # response = await self.async_post(self.clear_url, headers=self.headers, data=payload)  # 先做一次clear

        random_id = (
            str(round(time.time() * 1000)) + "_" +
            str(random.randint(10000, 99999))
        )
        payload = {
                    "type": "message",
                    "data": {
                        "question": messages[-1]["content"],
                        "sessionId": "kkbot-session" + random_id,
                        "appId": self.appId,
                        "questionId": random_id,
                    },
            }


        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )
            # print("resp", resp)
            
            if isinstance(resp, dict):
                return resp
            response_reslut = {
                "code": -1,
                "message": "",
            }
            data_p = re.compile("data: (.*?)\n")
            data_list = re.findall(data_p, resp)
            
            for data in data_list:
                json_string = data

                response_data = json.loads(json_string.strip())

                if response_data["code"] == 200:
                    response_reslut["message"] += response_data["data"]["result"]
                    if response_data['data']['type'] == 'sensitive':
                        break
                    

                elif response_data["code"] == 205:
                    # 召回知识 其实好像没什么用
                    continue
                elif response_data["code"] == 201 and "data" not in response_data.keys():
                    break

            if response_reslut["code"] == -1:
                response_reslut["code"] = 200
            resp = response_reslut

        except Exception as e:

            return e
        return resp



    def parse(self, response):
        try:
            if response["code"] != 200:
                return (False, response["message"])

            return (
                True,
                response["message"],
            )
        except Exception as e:
            return e
