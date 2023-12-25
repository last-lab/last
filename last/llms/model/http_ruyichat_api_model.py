"""
   昶甘信息 ruyichat API 
"""
import re
import json
from .base_model import HTTPAPILLMModel


class RuyichatAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        params: dict = json.loads(api_key)
        # params ---------------------------
        self.source = params["source"]
        self.version = params["version"]
        self.mc = params["mc"]
        self.uid = params["uid"]
        self.devid = params["devid"]
        self.verifyCode = params["verifyCode"]
        # params ---------------------------
        self.url = f"https://gptapi.ruyichat.com/v6/questionanswer?source={self.source}&version={self.version}&mc={self.mc}&uid={self.uid}&devid={self.devid}&verifyCode={self.verifyCode}"
        self.headers = {
            "Content-Type": "application/json",
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "input": messages[-1]["content"],
            "conversation_id": f"{self.uid}_{self.devid}_20231225",
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
        p_status = re.compile('{"data":.*?,"info":"(.*?)","status":(.*?)}')
        p_data = re.compile('{"data":{"id":".*?","content":"(.*?)"},"info":"(.*?)","status":(.*?)}')
        status_data_list = re.findall(p_status, response)
        # status_data_list =[('登录信息无效', '0')]
        for item in status_data_list:
            if int(item[1]) != 1:
                return (False, item[0])
        # 输出
        data_list = re.findall(p_data, response)
        # data_list = [('中', 'success', '1'), ('的', 'success', '1')]
        tmp_str = ""
        
        for item in data_list:
            if int(item[2]) != 1:
                return (False, "error")
            tmp_str += item[0]
        return (True, tmp_str)
