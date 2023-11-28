"""
   商汤LLM
   pip install PyJWT
"""
import jwt
import json
import time
from .base_model import HTTPAPILLMModel


def encode_jwt_token(ak, sk):
    headers = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 90000,  # 填写您期望的有效时间，此处示例代表当前时间+30分钟
        "nbf": int(time.time()) - 5,  # 填写您期望的生效时间，此处示例代表当前时间-5秒
    }
    token = jwt.encode(payload, sk, headers=headers)
    return token


class ShangtangAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://api.sensenova.cn/v1/llm/chat-completions"
        param = json.loads(api_key)
        ak = param["ak"]  # 填写您的ak
        sk = param["sk"]  # 填写您的sk
        self.token = encode_jwt_token(ak, sk)
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": self.token,
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
            "max_new_tokens": 1024,
            "messages": formatted_messages,
            "model": "nova-ptc-xl-v1",
            "repetition_penalty": 1.05,
            "stream": False,
            "temperature": 0.8,
            "top_p": 0.7,
        }
        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )

        except Exception as e:
            return e
        return resp

    def parse(self, response):
        if "error" in response:
            return (False, response["error"]["message"])
        # print(response)
        return (
            True,
            response["data"]["choices"][0]["message"],
        )
