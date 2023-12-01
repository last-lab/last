
"""
   百度 ERINEBOT API ak sk有时间限制, 过期无效
"""
import json
from .base_model import HTTPAPILLMModel


class ERNIEBOTAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        param = json.loads(api_key)
        self.ak = param["ak"]
        self.sk = param["sk"]
        self.url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token="
        self.headers = {
            "Content-Type": "application/json",
        }
    
    async def get_access_token(self):
        """
        使用 API Key, Secret Key 获取access_token, 替换下列示例中的应用API Key、应用Secret Key
        """            
        url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={self.ak}&client_secret={self.sk}"
        
        payload = '{}'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        try:
            resp = await self.async_post(
                url, headers=headers, data=json.dumps(payload)
            )
        except Exception as e:
            return e
        return resp.get("access_token")


    async def generate(self, prompt, messages, *args, **kwargs):
        try:
            access_token = await self.get_access_token()

        except Exception as e:
            return e
        

        self.url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=" + access_token
        formatted_messages = [
            {
                "role": item["role"],
                "content": item["content"],
            }
            for item in messages
        ]
        
        
        payload = {
            "messages": formatted_messages,
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
        if response is None or 'error_code' in response:
            return (False, response['error_msg'])
        return (
            True,
            response['result'],
        )
