from typing import List, Dict, Union, Optional, Tuple
from .base import Record, Statistics, BaseModel
from .public import ReturnCode
from .dataset import Message, MessageRole
from pydantic import BaseModel, Field
from last.services.enums import StrEnum
import asyncio
import json
import requests


class LLMType(StrEnum):
    critic = "critic"
    normal = "normal"
    attacker = "attacker"


# 这个类里面的东西是专门用来display的
class LLMInfo(Record):
    name: Optional[str] = Field(default=None)  # 如果多个模型str用换行符隔开
    model_type: Optional[LLMType] = Field(default=None)
    version: Optional[str] = Field(default=None)
    base_model: Optional[str] = Field(default=None)
    parameter_volume: Optional[str] = Field(default=None)
    pretraining_info: Optional[str] = Field(default=None)
    finetuning_info: Optional[str] = Field(default=None)
    alignment_info: Optional[str] = Field(default=None)

    endpoint: str
    access_key: str
    secret_key: Optional[str] = Field(default=None)


class Registration(Record):
    context: str  # 二进制字符串


class LLM(LLMInfo):
    registration: Optional[Registration] = Field(default=None)

    """Model name to use."""
    temperature: Optional[float] = 0.7
    """What sampling temperature to use."""
    organization: Optional[str] = None
    # to support explicit proxy for OpenAI
    proxy: Optional[str] = None
    request_timeout: Optional[Union[float, Tuple[float, float]]] = None
    """Timeout for requests to OpenAI completion API. Default is 600 seconds."""
    max_retries: Optional[int] = 6
    """Maximum number of retries to make when generating."""
    streaming: Optional[bool] = False
    """Whether to stream the results or not."""
    n: Optional[int] = 1
    """Number of chat completions to generate for each prompt."""
    max_tokens: Optional[int] = None
    """Maximum number of tokens to generate."""
    max_token_length: Optional[int] = Field(default=None)  # 单句 最大token长度
    max_access_per_hour: Optional[int] = Field(default=None)  # 每小时最大访问次数
    max_access_per_min: Optional[int] = Field(default=None)  # 每分钟最大访问次数

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def __call__(self, *msgs: Message) -> Message:
        # 先mock一下
        if self.model_type is LLMType.critic:
            prompt = self.gen_similarity_prompt(*msgs)
        else:
            prompt = msgs[0].content
        return_msg = await self.generate(prompt)
        return return_msg

    async def generate(self, msg: str) -> Message:
        # TODO SystemMessage的支持
        # 整个函数现在的Mock的以后开发
        return_msg = await self.puyu(msg)
        return_msg = Message(role=MessageRole.AI, content=return_msg)
        return return_msg

    def gen_similarity_prompt(self, responce: Message, correct_ans: Message) -> str:
        prompt = f"请根据语义的相似度比较实际答案和标准答案之间的差异，评分范围0.0~10.0。实际答案：{responce.content}；标准答案：{correct_ans.content}"
        return prompt

    async def puyu(self, prompt: str) -> str:
        # token = subprocess.check_output(["openxlab", "token"]).decode('utf8').strip()
        # print(token)

        # 'https://puyu.openxlab.org.cn/puyu/api/v1/chat/completion'
        # "Bearer eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiIwNDkzOTEiLCJyb2wiOiJST0xFX1JFR0lTVEVSIiwiaXNzIjoiT3BlblhMYWIiLCJpYXQiOjE2OTU2NDE5MzAsInBob25lIjoiMTk5MDE2NzA1MzIiLCJhayI6InZ5N2tvcWJ2cGd4MGFhbnFlYmR6IiwiZW1haWwiOiJ3YW5neHVob25nQHBqbGFiLm9yZy5jbiIsImV4cCI6MTY5NTY0NTUzMH0.7BI5-qt35B9XDKb14KV_X_LmiJr1IpDws2mkzGIO7wWComHEnHoXh0Yn3f5P-iHOMoiJIMgqhqeZaXJFrjb9QQ"

        header = {"Content-Type": "application/json", "Authorization": self.access_key}
        data = {
            "model": "ChatPJLM-latest",
            "messages": [{"role": "user", "text": prompt}],
            "n": 1,
            "temperature": 0.8,
            "top_p": 0.9,
            "disable_report": False,
        }
        try:
            res = await requests.post(self.endpoint, headers=header, data=json.dumps(data))       
            if res.status_code == 200:
                return res.json()["data"]["choices"][0]["text"]
            else:
                return res.json()["msg"]
        except:
            return 'Network Error'