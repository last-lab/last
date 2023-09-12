from typing import List, Dict, Union, Optional, TypeVar
from pydantic import BaseModel

from .base import Record, Statistics, BaseManager
from .public import RiskDimension, ReturnCode
from datetime import datetime


T = TypeVar('T', bound='Dataset')

class Message(Record):
    predecessor_uid: Optional[str] = None # 关联上一条Message记录的id
    successor_uid: Optional[str] = None # 关联下一条Message记录的id
    role: str 
    content: str
    

class Dataset(Record, BaseManager):
    name: str
    dimensions: List[RiskDimension]
    url: str
    volume: str # 数据集大小
    used_by: Optional[List[str]]
    qa_record: Dict[str, Message]  # Message的唯一id

    def __post_init__(self):
        # 将新建的Dataset对象同步到DB中
        Dataset.new(Dataset)
        self.current_index = 0

    @staticmethod
    def edit(uid, conf: T) -> ReturnCode:  # 编辑数据集信息，返回状态码
        # 根据提供的id获取记录
        records = Dataset.get_records([uid])
        if not records:
            return ReturnCode.NOT_FOUND
        record = records[0]  # 获取唯一的记录
        # 更新记录的相关字段
        record.name = conf.name
        record.dimensions = conf.dimensions
        record.url = conf.url
        record.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 更新记录到数据库，这里假设有一个名为update_record的静态方法来更新数据库
        Dataset.update_record(record)

        return ReturnCode.SUCCESS

    @staticmethod
    def update_record(record: Record):
        # 根据record的uid将其更新到数据库中
        # 通过ORM实现数据库更新的逻辑
        pass


    @staticmethod
    def upload(content) -> str:  # 上传一份数据集，返回数据集id
        qa_url = Dataset.get_url(content)
        dataset = Dataset(name="xxx", dimensions="xxxx", url=qa_url)
        return dataset.uid

    @staticmethod
    def get_url(content) -> str:  # 上传一些文本content，返回url
        pass


    def __iter__(self):
        return self

    def __next__(self) -> Message:
        pass


