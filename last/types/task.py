from typing import List, Dict, Union, Optional, TypeVar
from pydantic import BaseModel, Field
from enum import Enum

from .llm import LLM, Registration
from .plan import Plan
from .base import Record, Statistics, BaseManager
from .public import UserInfo, StateCode, ReturnCode, ID
from .dataset import QARecord


T = TypeVar("T", bound="Task")


class Report(Record):  # 评测报告PDF
    context: str  # 二进制字符串


class Task(Record, BaseManager):
    plan_id: Optional[str] = Field(default=None, init=False)
    plan: Plan  # 方案
    state: Optional[StateCode] = Field(default=StateCode.In_Progress)
    report: Optional[Report] = Field(default=None)  # 评测报告

    llm_id: Optional[str] = Field(default=None, init=False)
    llm_model: LLM  # 如何查备案文件： LLM.registration->PDF的二进制编码

    critic_id: Optional[str] = Field(default=None, init=False)
    critic_model: LLM
    results: Dict[str, QARecord]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plan_id = self.plan.uid
        self.llm_id = self.llm_model.uid
        self.critic_id = self.critic_model.uid

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
