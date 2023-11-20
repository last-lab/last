"""
   小红书LLM API 
"""
import json
from .base_model import HTTPAPILLMModel


class XiaoHongShuAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://test823.xiaohongshu.com/xhs_llm/generate"
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        format_message = []

        for item in messages:
            if item["role"] == "user":
                format_message.append(
                    {
                        "sender_type": "USER",
                        "text": item["content"],
                    }
                )
            else:
                # bot 其实这个地方我也不知道除了user还有什么其他的
                format_message.append(
                    {
                        "sender_type": "BOT",
                        "text": item["content"],
                    }
                )

        payload = {
            "messages": format_message,
            "max_tokens": 256,
        }
        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )

        except Exception as e:

            return e
        return resp

    def parse(self, response):

        if response['reason'] == "request failed, rejected by auditor":
            return (True, response["reason"])
        elif response["status"] != "success":
            return (False, response["reason"])
        return (True, response["reply"])
