"""
   心海舟楫模型 API
"""
import json
from .base_model import HTTPAPILLMModel


class FerryAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = 'https://u158554-93f6-e7db67eb.bjb1.seetacloud.com:8443/ferry_chat/start_inference'
        self.api_key = api_key
        self.headers = {
            "Content-Type": "application/json",
            # "Authorization": self.api_key
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "text": messages[-1]["content"],
            'history': [], 
            'temperature': 0.8,
            'top_p': 1,
            'max_token_length': 4096,
            'tokens_to_generate': 1024,
            'user_id': 'shj1pO4d'
        }
        try:
            resp = await self.async_post(
                self.url, headers=self.headers, data=json.dumps(payload)
            )
            response = resp
            if response["status"] == "STARTED":
                task_id = response['task_id']
                VALID_USER_ID = 'Y4Qw1Pgd'
                url = f'https://u158554-93f6-e7db67eb.bjb1.seetacloud.com:8443/ferry_chat/check_inference/{task_id}?user_id={VALID_USER_ID}'
                status = "RUNNING"
                import requests
                retry_max = 3
                retry_count = 0
                # requests.get 在 asyncio 中是非阻塞的，这里用 time.sleep来被动阻塞
                while status == "RUNNING" and retry_count < retry_max:
                    import time
                    time.sleep(1)
                    retry_count += 1
                    resp = requests.get(
                        url
                    )
                    response = resp.json()
                    status = response['status']
                    if status != "RUNNING":
                        break
                    else:
                        time.sleep(2)
        except Exception as e:
            print("response[\"status\"] != \"COMPLETED\"")
            return e
        return response

    def parse(self, response):
        if response["status"] != "COMPLETED":
            return (False, "response[\"status\"] != \"COMPLETED\"")
        return (True, response["result"])
