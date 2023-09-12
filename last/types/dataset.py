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
    conversation_start_id: List[str] # 每段对话的起始Message id

    @property
    def length(self):
        return len(self.qa_record)
    
    def __iter__(self):
        self.current_conversation_index = 0
        self.current_message_id = self.conversation_start_id[0]
        return self

    def __next__(self) -> Message:
        # 每次迭代时，只输出一条Messsage消息，
        # 第一次迭代的时候，输出第一个conversation里面的第一条消息
        # 下次迭代时，输出第二条消息
        # 如果当前conversation已经迭代完毕（即successor_uid为None），则输出第二个conversation里面的第一条消息
        # 直到所有的conversation输出完毕
        if self.current_conversation_index >= len(self.qa_record):
            raise StopIteration

        message = self.qa_record[self.current_message_id]

        if message.successor_uid is None:
            self.current_conversation_index += 1
            if self.current_conversation_index < len(self.conversation_start_id):
                self.current_message_id = self.conversation_start_id[self.current_conversation_index]
        else:
            self.current_message_id = message.successor_uid
        return message

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





