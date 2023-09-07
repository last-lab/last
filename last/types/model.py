from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel

from .base import Record, Statistics
from .public import ReturnCode


@dataclass
class APIModelInfo(Record):
    name: str
    model_type: str
    version: str
    base_model: str
    parameter_volume: str
    pretraining_info: str  # TODO 这里记得让UI改
    finetuning_info: str
    alignment_info: str
    # 下面的信息暂时不予显示
    API_url: str
    access_key: str
    secret_key: str
    max_token_length: int  # 单句最大token长度
    limited_token: int  # token余量
    max_access_per_hour: int  # 每小时最大访问次数
    max_access_per_min: int  # 每分钟最大访问次数

    registration: Optional[Registration] = None


@dataclass
class Registration(Record):
    context: str  # 二进制字符串
