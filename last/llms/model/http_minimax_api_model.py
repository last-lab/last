
"""
   minimax API
"""
import json
from .base_model import HTTPAPILLMModel


class MinimaxAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        param = json.loads(api_key)
        self.group_id = param["group_id"]
        self.api_key = param["api_key"]

        self.url = f'https://api.minimax.chat/v1/text/chatcompletion?GroupId={self.group_id}'
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        self.qps = 1

    async def generate(self, prompt, messages, *args, **kwargs):
        
        formatted_messages = list()
        for item in messages:
            if item["role"] == "user":
                formatted_messages.append(
                    {
                        "sender_type": "USER",
                        "text": item["content"],
                    }
                )
            else:
                formatted_messages.append(
                    {
                        "sender_type": "BOT",
                        "text": item["content"],
                    }
                )
        
        payload = {
            "model": "abab5-chat",
            "messages": formatted_messages,
            "tokens_to_generate": 512,
            **kwargs,
        }
        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )
            
        except Exception as e:
 
            return e
        return resp

    def parse(self, response):
        response = json.loads(response)
        if response is None or (response['base_resp']['status_code'] != 0 and response['base_resp']['status_code'] != 1027):
            return (False, response['base_resp']['status_msg'])
        
        if response['base_resp']['status_code'] == 1027:
            return (
                True,
                "输出包含敏感信息",
            )
        return (
            True,
            response['reply'],
        )
