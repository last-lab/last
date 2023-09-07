from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod
from tortoise.models import Model as ORMModel

from .public import DateString, PermissionLevel, UserInfo

@dataclass
class Record(BaseModel):
    uid: str # UUID-4
    description: Optional[str]
    creator: UserInfo
    editor: UserInfo
    reviewer: UserInfo
    created_at: DateString
    updated_at: DateString
    permissions: PermissionLevel

@dataclass
class Statistics(BaseModel):
    total_cnt: str
    updated_at: DateString
    description: Optional[str]

def create_ORM(db_url: str, user:UserInfo) -> ORMModel:
    pass


@dataclass
class Filter(BaseModel):
    field: str # 要筛选的字段
    operator: str  # 筛选操作符，如果是"between"则代表是可比较大小的筛选，如果是“equal”则是匹配筛选
    context: Union[str, List[str]]   #如果是单个字符串则代表匹配筛选，如果是一对字符串则代表区间筛选

class BaseManager(ABC):
    @staticmethod
    # 所有搜索功能采用智能模糊搜索或向量搜索，不做太多定义
    def find_records(orm: ORMModel, page_num: int, page_size:int , searched_by: Optional[str] =None, filted_by: Optional[List[Filter]] =None, sorted_by: Optional[List[str]] =None) -> List[str]: # 返回满足要求的id
        pass

    @staticmethod
    def get_records(orm: ORMModel, ids:List[str]) -> List[Record]: # 根据id查记录
        pass

    @staticmethod
    def new(orm: ORMModel, conf: Record) -> str: # 返回新创建的uid
        pass

    @staticmethod
    def export(orm: ORMModel, id:str) -> str: # 文件下载地址
        pass

    @staticmethod
    def delete(orm: ORMModel, id:str) -> ReturnCode: # 返回行为码
        pass




