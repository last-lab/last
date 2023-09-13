from typing import List, Dict, Union, Optional, TypeVar, Tuple
from dataclasses import dataclass
from .base import Record, Statistics, BaseManager
from .public import RiskDimension, ReturnCode, ID
from datetime import datetime
from pathlib import Path
from pydantic import HttpUrl, Field, validator
import csv
from enum import Enum

T = TypeVar('T', bound='Dataset')

class MessageRole(str, Enum):
    System = "System"
    AI = "AI"
    Human = "Human"
    Chat = "Chat"

class Message(Record):
    role: MessageRole
    content: str

class QARecord(Record):
    predecessor_uid: Optional[str] = None # 关联上一条Message记录的id
    successor_uid: Optional[str] = None # 关联下一条Message记录的id
    question: Message
    answer: Optional[Message] = None


class Dataset(Record, BaseManager):
    name: str
    dimensions: List[RiskDimension]
    url: Optional[HttpUrl] = None # 文件url
    file: Optional[Path] = None # 文件本地path
    volume: Optional[str] = None # 数据集大小
    used_by: Optional[List[str]] = None
    qa_record: Optional[Dict[str, QARecord]] = None  # Message的唯一id
    conversation_start_id: Optional[List[str]] = None # 每段对话的起始Message id
    current_conversation_index: Optional[int] = Field(default=0, init=False) # 供迭代器使用
    current_message_id: Optional[int] = Field(default=0, init=False) # 供迭代器使用

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.post_init()  

    def post_init(self):
        # 根据传入的url或者file path，新建Dataset对象
        if self.file is not None:
            self.qa_record, self.conversation_start_id = Dataset.upload(self.file)
        elif self.url is not None:
            self.qa_record, self.conversation_start_id = Dataset.fetch(self.url)
        else:
            raise ValueError("Input parameter cannot be empty")

    @property
    def length(self):
        return len(self.qa_record)
    
    def __iter__(self):
        self.current_conversation_index = 0
        self.current_message_id = self.conversation_start_id[0]
        return self

    def __next__(self) -> QARecord:
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
    def fetch(url: HttpUrl):
        # 通过访问url创建数据集
        pass


    @staticmethod
    def upload(file_path: Path) -> Tuple[Dict[str, QARecord], List[str]]:  
        # 通过上传文件创建数据集
        qa_record = {}
        predecessor_uid = None # 关联上一条Message记录的id
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self_uid = ID()
                question = Message(role=MessageRole.Human, content=row["question"])
                correct_ans = Message(role=MessageRole.AI, content=row["correct_ans"])
                successor_uid = ID() # 提前安排好下一条数据的ID
                qa_record[self_uid] = QARecord(predecessor_uid=predecessor_uid, successor_uid=successor_uid, question=question, answer=correct_ans)
                predecessor_uid = self_uid 
            conversation_start_id = list(qa_record.keys())
        return qa_record, conversation_start_id





