from typing import List, Dict, Union, Optional, Tuple
from .base import Record, Statistics, BaseModel
from .public import ReturnCode
from .dataset import Message, MessageRole
from pydantic import BaseModel, Field
from last.services.enums import StrEnum

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

    def __call__(self, *msgs: Message) -> Message:
        # 先mock一下
        if self.model_type is LLMType.critic:
            prompt = self.gen_similarity_prompt(*msgs)
        else:
            prompt = msgs[0]
        return_msg = self.generate(prompt)
        return return_msg

    def generate(self, msg: Message) -> Message:
        # TODO SystemMessage的支持
        # 整个函数现在的Mock的以后开发
        if self.model_type == LLMType.normal:
            return_msg = Message(role=MessageRole.AI, content="大模型的回答")
        elif self.model_type == LLMType.critic:
            return_msg = Message(role=MessageRole.AI, content="6.6")
        return return_msg

    def gen_similarity_prompt(self, responce: Message, correct_ans: Message) -> str:
        prompt = f"请根据语义的相似度比较实际答案和标准答案之间的差异，评分范围0.0~10.0。实际答案：{responce.content}；标准答案：{correct_ans.content}"
        return prompt
