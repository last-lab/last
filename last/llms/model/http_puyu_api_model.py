import json
import requests
from .base_model import HTTPAPILLMModel


class PuyuAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://puyu.openxlab.org.cn/puyu/api/v1/chat/completion"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        formatted_messages = [
            {
                "role": item["role"],
                "text": item["content"],
            }
            for item in messages
        ]

        payload = {
            "model": "ChatPJLM-latest",
            "messages": formatted_messages,
            **kwargs,
        }
        return requests.post(
            self.url, headers=self.headers, data=json.dumps(payload)
        ).json()

    def parse(self, response):
        return (
            response["msg"] == "success",
            response["data"]["choices"][0]["text"],
        )
