from typing import List, Dict, Union, Optional, Tuple

import last.types.prompt_template
from .base import Record, Statistics, BaseModel
from .public import ReturnCode
from .dataset import Message, MessageRole
from pydantic import BaseModel, Field
from last.services.enums import StrEnum
import asyncio
from last.client.call_llm import generate
from last.types.prompt_template import PromptGenerator

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
    system_prompt: Optional[str] = Field(default=None)


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

    async def __call__(self, *msgs: Message) -> Message:
        # 提供 model 部分信息生成 prompt
        self.system_prompt, prompt = PromptGenerator.generate_prompt(self.name, self.model_type, *msgs)
        print("********************************")
        print(self.system_prompt)
        return_msg = await generate(
            prompt=prompt,
            model=self.name,
            system_prompt=self.system_prompt,
            maximum_length=self.max_tokens,
        )
        return_msg = Message(role=MessageRole.AI, content=return_msg)
        return return_msg
