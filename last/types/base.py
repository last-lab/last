from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod

from .public import DateString, PermissionLevel, UserInfo


@dataclass
class Record(BaseModel):
    uid: Optional[str] = None  # UUID-4
    description: Optional[str] = None
    creator: UserInfo
    editor: Optional[UserInfo] = None
    reviewer: Optional[UserInfo] = None
    created_at: DateString
    updated_at:  Optional[DateString] = None
    permissions: PermissionLevel


@dataclass
class Statistics(BaseModel):
    total_cnt: str
    updated_at: DateString
    description: Optional[str] = None


@dataclass
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


class BaseModel(ABC):
    """Base class for Chat models."""
    pass