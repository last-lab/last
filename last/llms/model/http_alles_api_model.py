import json
import requests
from .base_model import HTTPAPILLMModel


class AllesMinimaxAPILLMModel(HTTPAPILLMModel):
    map_dict = {"user": "USER"}

    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://openxlab.org.cn/gw/alles-apin/v1/minimax/v1/text/chat"
        self.headers = {
            "Content-Type": "application/json",
            "alles-apin-token": api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        formatted_messages = [
            {
                "sender_type": self.map_dict[item["role"]],
                "text": item["content"],
            }
            for item in messages
        ]

        payload = {
            "model": "abab5-chat",
            "prompt": " ",  # TODO
            "messages": formatted_messages,
            "role_meta": {"user_name": "user", "bot_name": "assistant"},
            "type": "json",
            **kwargs,
        }
        result = await self.async_post(
            self.url, headers=self.headers, data=json.dumps(payload)
        )
        if result["msgCode"] == "10000":
            return result
        else:
            raise ValueError(result.text)

    def parse(self, response):
        return (
            True,
            response["data"]["choices"][0]["text"],
        )


class AllesChatGPTAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://ecs.sv.us.alles-apin.openxlab.org.cn/v1/openai/v2/text/chat"
        self.headers = {
            "Content-Type": "application/json",
            "alles-apin-token": api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            **kwargs,
        }
        result = await self.async_post(
            self.url, headers=self.headers, data=json.dumps(payload)
        )
        if result["msgCode"] == "10000":
            return result
        else:
            raise ValueError(result.text)

    def parse(self, response):
        return (
            True,
            response["data"]["choices"][0]["message"]["content"],
        )


class AllesGPT4APILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://ecs.sv.us.alles-apin.openxlab.org.cn/v1/openai/v2/text/chat"
        self.headers = {
            "Content-Type": "application/json",
            "alles-apin-token": api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "model": "gpt-4",
            "messages": messages,
            **kwargs,
        }
        result = await self.async_post(
            self.url, headers=self.headers, data=json.dumps(payload)
        )
        if result["msgCode"] == "10000":
            return result
        else:
            raise ValueError(result.text)

    def parse(self, response):
        return (
            True,
            response["data"]["choices"][0]["message"]["content"],
        )


class AllesPalmAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://ecs.sv.us.alles-apin.openxlab.org.cn/v1/google/v1/palm/chat"
        self.headers = {
            "Content-Type": "application/json",
            "alles-apin-token": api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        formatted_messages = [
            {
                "author": item["role"],
                "content": item["content"],
            }
            for item in messages
        ]

        payload = {
            "model": "chat-bison-001",
            "prompt": {
                "messages": formatted_messages,
            },
            "temperature": kwargs["temperature"],
            "candidate_count": 1,
        }
        result = await self.async_post(
            self.url, headers=self.headers, data=json.dumps(payload)
        )
        if result["msgCode"] == "10000":
            return result
        else:
            raise ValueError(result.text)

    def parse(self, response):
        return (
            True,
            response["data"]["candidates"][0]["content"],
        )


class AllesClaudeAPILLMModel(HTTPAPILLMModel):
    '''
        Only support English
    '''
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "http://ecs.sv.us.alles-apin.openxlab.org.cn/v1/claude/v1/text/chat"
        self.headers = {
            "Content-Type": "application/json",
            "alles-apin-token": api_key,
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
            "model": "claude-1",
            "messages": messages,
            **kwargs,
        }
        result = await self.async_post(
            self.url, headers=self.headers, data=json.dumps(payload)
        )
        if result["msgCode"] == "10000":
            return result
        else:
            raise ValueError(result.text)

    def parse(self, response):
        return (
            True,
            response["data"]["completion"],
        )


class AllesWenxinAPILLMModel(HTTPAPILLMModel):
    '''
        2023-10-27: This request is blocked by Alles-APIN due to auth failed.
    '''
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = (
            "https://openxlab.org.cn/gw/alles-apin/v1/baidu/v1/wenxinworkshop/chat"
        )
        self.headers = {
            "Content-Type": "application/json",
            "alles-apin-token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4LCJ1c2VybmFtZSI6ImxpdWt1aWt1biIsImFwcGx5X2F0IjoxNjg1NTE4OTY0MjA4LCJleHAiOjE4NjY5NTg5NjR9.Rb1jHeoPiYqplsn1Qk1rgPbOiNeovtCFwHa92YPR3Xo",
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "messages": messages,
            "stream": False,
            "user": "pjlab-alles-apin",
            # **kwargs,
        }
        result = await self.async_post(
            self.url, headers=self.headers, data=json.dumps(payload)
        )
        if result["msgCode"] == "10000":
            return result
        else:
            raise ValueError(result.text)

    def parse(self, response):
        return (
            response["data"] != "error",
            response["data"],
        )


class AllesSparkAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://openxlab.org.cn/gw/alles-apin/v1/xunfei/v1/spark/chat"
        self.headers = {
            "Content-Type": "application/json",
            "alles-apin-token": api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {
            "parameter": {
                "chat": {
                    "temperature": kwargs["temperature"],
                    "max_tokens": kwargs["max_tokens"],
                    "chat_id": "user",
                }
            },
            "payload": {"message": {"text": messages}},
        }
        result = await self.async_post(
            self.url, headers=self.headers, data=json.dumps(payload)
        )
        if result["msgCode"] == "10000":
            return result
        else:
            raise ValueError(result.text)

    def parse(self, response):
        return (
            response["data"] != "error",
            response["data"],
        )


class AllesBaiduTranslateAPILLMModel(HTTPAPILLMModel):
    def __init__(self, api_key, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = "https://openxlab.org.cn/gw/alles-apin/v1/baidu/v1/trans/general"
        self.headers = {
            "Content-Type": "application/json",
            "alles-apin-token": api_key,
        }

    async def generate(self, prompt, messages, *args, **kwargs):
        payload = {"q": prompt, "frm": "auto", "to": "en"}
        result = await self.async_post(
            self.url, headers=self.headers, data=json.dumps(payload)
        )
        if result["msgCode"] == "10000":
            return result
        else:
            raise ValueError(result.text)

    def parse(self, response):
        return (
            True,
            response["data"]["trans_result"][0]["dst"],
        )
