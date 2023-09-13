from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod
from last.client import Client

from .public import DateString, PermissionLevel, UserInfo, ReturnCode
from datetime import datetime


class Record(BaseModel):
    uid: Optional[str]  # UUID-4
    description: Optional[str]
    creator: Optional[UserInfo]
    editor: Optional[UserInfo]
    reviewer: Optional[UserInfo]
    created_at: Optional[DateString]
    updated_at:  Optional[DateString]
    permissions: Optional[PermissionLevel] = PermissionLevel.VIEWER

    def __init__(self, **data):
        if "created_at" not in data:
            now = datetime.now()
            data["created_at"] = DateString(
                year=str(now.year),
                month=str(now.month),
                day=str(now.day),
                hour=str(now.hour),
                minute=str(now.minute),
                second=str(now.second),
            )
        super().__init__(**data)


class Statistics(BaseModel):
    total_cnt: str
    updated_at: DateString
    description: Optional[str]



class Filter(BaseModel):
    field: str  # 要筛选的字段
    operator: str  # 筛选操作符，如果是"between"则代表是可比较大小的筛选，如果是“equal”则是匹配筛选
    context: Union[str, List[str]]  # 如果是单个字符串则代表匹配筛选，如果是一对字符串则代表区间筛选


class BaseManager(ABC):
    @staticmethod
    # 所有搜索功能采用智能模糊搜索或向量搜索，不做太多定义
    def find_records(
        page_num: int,
        page_size: int,
        searched_by: Optional[str] = None,
        filted_by: Optional[List[Filter]] = None,
        sorted_by: Optional[List[str]] = None,
    ) -> List[str]:  # 返回满足要求的id
        pass

    @staticmethod
    def get_records(ids: List[str]) -> List[Record]:  # 根据id查记录
        pass

    @staticmethod
    def new(conf: Record) -> str:  # 返回新创建的uid
        pass

    @staticmethod
    def export(id: str) -> str:  # 文件下载地址
        pass

    @staticmethod
    def delete(id: str) -> ReturnCode:  # 返回行为码
        pass
