from typing import List, Dict, Union, Optional, TypeVar
from pydantic import BaseModel, Field
from enum import Enum

from .llm import LLM, Registration
from .plan import Plan
from .base import Record, Statistics, BaseManager
from .public import UserInfo, StateCode, ReturnCode, ID
from .dataset import QARecord


T = TypeVar('T', bound='Task')


class TaskDetail(Record):
    context: str  # 二进制字符串

class Task(Record, BaseManager):
    plan: Plan
    state: Optional[StateCode] = Field(default=StateCode.In_Progress)
    report_detail: Optional[TaskDetail] = Field(default=None)
    model_detail: LLM
    critic_model: LLM
    results: Dict[str, QARecord]

    @staticmethod
    def repeat(id, conf: T) -> str:  # 因为某些异常，需要重新提交一次评测
        pass

    @staticmethod
    def load_model_api(model: LLM) -> ReturnCode:
        # 通过输入test prompt进行模型测试
        pass

    @staticmethod
    def check_state(id) -> StateCode:
        # 检查状态
        pass

    @staticmethod
    def open_registration(model_id) -> Registration:
        # 检查状态
        pass

    def render_report(self, file_path, type) -> None:
        pass



