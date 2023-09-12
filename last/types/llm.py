from typing import List, Dict, Union, Optional, Tuple
from .base import Record, Statistics, BaseModel
from .public import ReturnCode
from .dataset import Message
from enum import Enum

class LLMType(str, Enum):
    critic = "critic"
    normal = "normal"
    attacker = "attacker"

# 这个类里面的东西是专门用来display的
class LLMInfo(Record):
    name: str
    model_type: LLMType
    version: str
    base_model: str
    parameter_volume: str
    pretraining_info: str  
    finetuning_info: str
    alignment_info: str
    
    endpoint: str
    access_key: str
    secret_key: str

class Registration(Record):
    context: str  # 二进制字符串


class LLM(LLMInfo):
    registration: Optional[Registration] = None

    """Model name to use."""
    temperature: float = 0.7
    """What sampling temperature to use."""
    organization: Optional[str] = None
    # to support explicit proxy for OpenAI
    proxy: Optional[str] = None
    request_timeout: Optional[Union[float, Tuple[float, float]]] = None
    """Timeout for requests to OpenAI completion API. Default is 600 seconds."""
    max_retries: int = 6
    """Maximum number of retries to make when generating."""
    streaming: bool = False
    """Whether to stream the results or not."""
    n: int = 1
    """Number of chat completions to generate for each prompt."""
    max_tokens: Optional[int] = None
    """Maximum number of tokens to generate."""
    max_token_length: int  # 单句 最大token长度
    max_access_per_hour: int  # 每小时最大访问次数
    max_access_per_min: int  # 每分钟最大访问次数


    def __call__(self, *msgs:Message) -> Message:
        # 先mock一下
        if self.model_type is LLMType.critic:
            prompt = self.gen_similarity_prompt(*msgs)
        return_msg = self.generate(prompt)
        return return_msg

    def generate(self, msg:Message) -> Message:
        # TODO SystemMessage的支持
        return_msg = Message(predecessor_uid="83fba5b4-5c6d-4f88-a7d3-9e3d2c1f6b02", successor_uid="d8b1e6d7-9a0b-4c2f-8e3d-1f0e9b8c7a6d", role="assistant", content="大模型标准回答")
        return return_msg

    def gen_similarity_prompt(self, responce:Message, correct_ans:Message) -> str:
        prompt = f"请根据语义的相似度比较实际答案和标准答案之间的差异，评分范围0.0~10.0。实际答案：{responce.content}；标准答案：{correct_ans.content}"
        return prompt

