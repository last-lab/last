"""
   大智慧惠问 xiaohui API
"""
import json
# from .base_model import HTTPAPILLMModel


# class XiaohuiAPILLMModel(HTTPAPILLMModel):
#     def __init__(self, api_key, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.url = "https://api-bz7ic07j.tigerbot.com/v1/chat/completions"
#         self.api_key = api_key
#         self.headers = {
#             "Content-Type": "application/json",
#             "Authorization": "Bearer " + self.api_key,
#         }

#     async def generate(self, prompt, messages, *args, **kwargs):
#         payload = {
#             "model": "tigerbot-70b-chat",
#             "query": messages[-1]["content"],
#             **kwargs,
#         }
#         try:
#             resp = await self.async_post(
#                 self.url, headers=self.headers, data=json.dumps(payload)
#             )
            
#         except Exception as e:
 
#             return e
#         return resp

#     def parse(self, response):
#         if "error" in response:
#             return (False, response["error"]["message"])

#         return (
#             True,
#             response["result"],
#         )

# import requests

# url = "https://xiaohuiapi1.dzh.com.cn/xiaohui/answer?q=&token="
# headers = {
#     "Content-Type": "application/json",
# }
# resp = requests.post(url=url, headers=headers, data=json.dumps({}))

# print(resp.json())
# resp_get = requests.get(
#     url="https://xiaohuiapi1.dzh.com.cn//xiaohui/search?q=&token=",
#     headers=headers,
#     data=json.dumps({}),
# )
# print(resp_get.json())