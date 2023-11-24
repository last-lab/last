import json
import subprocess
from .base_model import HTTPAPILLMModel


class PuyuAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://puyu.openxlab.org.cn/puyu/api/v1/chat/completion"
        param = json.loads(api_key)
        self.ak = param["AK"]
        self.sk = param["SK"]
        self.token = self.get_token(self.ak, self.sk)


        # self.token = param["appId"]

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": api_key,
        }

    def get_token(self, ak: str, sk: str):
        process = subprocess.Popen("openxlab config", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # 第一次用户输入
        user_input1 = ak + "\n"  # 第一次输入数据
        user_input2 = sk + "\n"  # 第二次输入数据

        # 检查子进程是否已经终止
        if process.poll() is None:
            process.stdin.write(user_input1)
            process.stdin.flush()
            process.stdin.write(user_input2)
            process.stdin.flush()
        else:
            # 处理子进程已经终止的情况
            print("浦语模型token无法获取")
        token = subprocess.run("openxlab token", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True).stdout
        return token

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
        response = await self.async_post(
            self.url, headers=self.headers, data=json.dumps(payload)
        ).json()
        return response

    def parse(self, response):
        return (
            response["msg"] == "success",
            response["data"]["choices"][0]["text"],
        )
