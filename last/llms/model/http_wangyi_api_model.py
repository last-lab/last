"""
   网易 易生诸相LLM API 
"""

import requests
import json
from .base_model import HTTPAPILLMModel


class WangYiAPILLMModel(HTTPAPILLMModel):
   def __init__(self, api_key, *args, **kwargs):
      super().__init__(*args, **kwargs)
      param = json.loads(api_key)
      self.cookies = {
         "RBAC_USER": param["RBAC_USER"],
         "RBAC_TOKEN": param["RBAC_TOKEN"],
      }
      self.url = "https://wangyifuxi.apps-cae.danlu.netease.com/yuyan/api/v1/msg"
      self.api_key = api_key
      self.headers = {
         "Content-Type": "application/json",
      }

   async def generate(self, prompt, messages, *args, **kwargs):
      formatted_messages = [
         {
            "role": item["role"],
            "content": item["content"],
         }
         for item in messages
      ]
      payload = {
            "type": 0,
            "content": formatted_messages,
            **kwargs,
      }
      try:
            resp = await self.async_post(
               self.url,
               headers=self.headers,
               data=json.dumps(payload),
               cookies=self.cookies,
            )

      except Exception as e:

            return e
      return resp

   def parse(self, response):
      if "content" not in response:
            return (False, response["codeName"])

      return (
            True,
            response["content"],
      )
