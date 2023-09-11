from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel

from .base import Record, Statistics, BaseModel
from .public import ReturnCode
from .dataset import Message


@dataclass
# 这个类里面的东西是专门用来display的
class ModelInfo(Record):
    name: str
    model_type: str
    version: str
    base_model: str
    parameter_volume: str
    pretraining_info: str  # TODO 这里记得让UI改
    finetuning_info: str
    alignment_info: str

    endpoint: str
    access_key: str
    secret_key: str
    max_token_length: int  # 单句最大token长度
    max_access_per_hour: int  # 每小时最大访问次数
    max_access_per_min: int  # 每分钟最大访问次数

    registration: Optional[Registration] = None


@dataclass
class Model(ModelInfo, BaseModel):
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


    def call(self, msg:Message) -> Message:
        return Message(related_uid = "xxcadasdad", role="assistant", content="大模型标准回答")


@dataclass
class Registration(Record):
    context: str  # 二进制字符串
