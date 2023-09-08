from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel

from .model import APIModelInfo
from .task import TaskInfo
from .base import Record, Statistics, BaseManager
from .public import UserInfo, StateCode, ReturnCode


@dataclass
class Report(Record, BaseManager):
    task: TaskInfo
    state: StateCode
    report_detail: Optional[ReportDetail] = None
    model_detail: APIModelInfo

    @staticmethod
    def repeat(id, conf: Report) -> str:  # 因为某些异常，需要重新提交一次评测
        pass

    @staticmethod
    def load_model_api(model: APIModelInfo) -> ReturnCode:
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

    @staticmethod
    def render(file_path, type) -> None:
        pass


@dataclass
class ReportDetail(Record):
    context: str  # 二进制字符串
