from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel
import torch
from tortoise.models import Model as ORMModel
                                                                              
from .model import ModelDetail, Registration
from .task import Task
from .base import Record, Statistics, BaseManager
from .public import UserInfo, StateCode, ReturnCode

@dataclass
class Report(Record):
    model_name: str
    version: str
    display_name: str
    task_name: str
    task_detail: Task
    state: StateCode
    report_detail: Optional[ReportDetail] = None
    model_detail: ModelDetail
    registration: Optional[Registration] = None
    

@dataclass
class ReportDetail(Record):
    context: str #二进制字符串


class ReportManager(BaseManager):
    @staticmethod 
    def repeat(orm: ORMModel, id, conf: Report) -> str: # 因为某些异常，需要重新提交一次评测
        pass

    @staticmethod
    def load_model_api(model:ModelDetail) -> ReturnCode:
        # 通过输入test prompt进行模型测试
        pass

    @staticmethod
    def check_state(rm: ORMModel, id) -> StateCode:
        # 检查状态
        pass

    @staticmethod
    def open_registration(orm: ORMModel, report_id, model_id) -> Registration:
        # 检查状态
        pass