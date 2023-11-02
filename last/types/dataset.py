from typing import List, Dict, Union, Optional, TypeVar, Tuple
from dataclasses import dataclass
from .base import Record, Statistics, BaseManager
from .public import RiskDimension, ReturnCode, ID
from datetime import datetime
from pydantic import HttpUrl, Field, validator, BaseModel
import csv
from enum import Enum
from last.services.enums import StrEnum
import os
import pandas as pd

DatasetTyping = TypeVar("DatasetTyping", bound="Dataset")


class MessageRole(StrEnum):
    System = "System"
    AI = "AI"
    Human = "Human"
    Chat = "Chat"


class Message(BaseModel):
    role: MessageRole
    content: str

    def __str__(self):
        return self.content


class Annotation(BaseModel):
    pass


class QARecord(BaseModel):
    predecessor_uid: Optional[str] = None  # 关联上一条Message记录的id, 用于多轮对话，目前不启用
    successor_uid: Optional[str] = None  # 关联下一条Message记录的id, 用于多轮对话，目前不启用
    question: Message
    answer: Optional[Message] = None
    critic: Optional[Message] = None  # critic模型对该条QARecord的回复
    annotation: Optional[Annotation] = None  # QARecord对应的人工标注结果


class Dataset(Record, BaseManager):
    name: Optional[str] = Field(default=None)  # 模型名称
    focused_risks: Optional[List[RiskDimension]] = Field(default=None)  # 风险详情
    url: Optional[HttpUrl] = None  # 文件导出url
    file: Optional[str] = None  # 文件本地path
    volume: Optional[str] = Field(default="0.0GB")  # 数据集大小GB
    used_by: Optional[int] = Field(default=0)  # 使用次数
    qa_num: Optional[int] = Field(default=0, init=False)  # 对话条数
    word_cnt: Optional[int] = Field(default=0, init=False)  # 语料字数

    qa_records: Optional[
        Dict[str, QARecord]
    ] = None  # key是每条QARecord的唯一id, 也是Dataset类中的实际内容存储

    conversation_start_id: Optional[
        List[str]
    ] = None  # 每段对话的起始QARecord id, 为了多轮对话，目前暂时不启用
    current_conversation_index: Optional[int] = Field(default=0, init=False)  # 供迭代器使用
    current_qa_record_id: Optional[int] = Field(default=0, init=False)  # 供迭代器使用

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.file is not None:  # 根据传入的file path，新建Dataset对象
            self.qa_records = Dataset.upload(self.file)
        elif self.qa_records is not None:  # 根据传入的qa_records，保存file文件
            os.makedirs(os.path.join("dashboard", "static", "saves"), exist_ok=True)
            file_path = os.path.join("dashboard", "static", "saves", f"{self.name}.csv")
            Dataset.write_dict_list_to_csv(self.qa_records, file_path)
            self.file = file_path
        else:
            raise ValueError("Input parameter cannot be empty")

        self.fill_attributes(self.qa_records)

    @staticmethod
    def write_dict_list_to_csv(qa_records, filename):
        # 获取所有的字段名
        fieldnames = ["question", "answer", "critic"]
        assert set(fieldnames).issubset(
            set(vars(qa_records[list(qa_records.keys())[0]]))
        )
        # 写入CSV文件
        with open(filename, mode="w", newline="", encoding="utf-8-sig") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # 写入字段名
            writer.writeheader()

            # 逐行写入字典数据
            for qa_record in qa_records.values():
                row = {field: str(getattr(qa_record, field)) for field in fieldnames}
                writer.writerow(row)

    @staticmethod
    def upload(file_path: str) -> Tuple[Dict[str, QARecord], List[str]]:
        # TODO 注释掉的部分是为了给多轮对话准备的，目前还没有经过测试，故不写
        # 通过上传文件创建数据集
        if file_path.endswith("csv"):
            qa_records = Dataset.read_csv(file_path)
        elif file_path.endswith("xlsx"):
            qa_records = Dataset.read_excel(file_path)
        return qa_records

    @staticmethod
    def read_csv(file_path):
        qa_records = {}
        # predecessor_uid = None # 关联上一条Message记录的id
        with open(file_path, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)
            for row in reader:
                self_uid = ID()
                question = Message(role=MessageRole.Human, content=row["question"])
                correct_ans = Message(
                    role=MessageRole.AI, content=row["correct_ans"]
                )
                # successor_uid = ID() # 提前安排好下一条数据的ID
                qa_records[self_uid] = QARecord(
                    predecessor_uid=None,
                    successor_uid=None,
                    question=str(question),
                    answer=str(correct_ans),
                )
                # predecessor_uid = self_uid
        return qa_records

    @staticmethod
    def read_excel(filename: str) -> Tuple[Dict[str, QARecord], List[str]]:
        qa_records = {}
        xls = pd.ExcelFile(filename)
        sheet_names = xls.sheet_names
        # Loop through all the sheets
        for sheet_name in xls.sheet_names:
            # Read the sheet into a DataFrame
            df = pd.read_excel(xls, sheet_name=sheet_name)
            for index, row in df.iterrows():
                qa_records[ID()] = QARecord(
                    predecessor_uid=None,
                    successor_uid=None,
                    question=Message(role=MessageRole.Human, content=str(row[0])),
                    answer=Message(role=MessageRole.Human, content=str(row[1])),
                )
            # key = df.keys()[0]  ### change for complex
            ####### change togather ####
        return qa_records

    # TODO 根据qa_records填充其他属性, 现在是mock的
    def fill_attributes(self, qa_records: Dict[str, QARecord]) -> None:
        self.conversation_start_id = list(self.qa_records.keys())
        self.qa_num = len(qa_records)
        self.word_cnt = Dataset.word_counting(qa_records)
        self.volume = str(os.path.getsize(self.file)) + "bytes"

    @staticmethod
    def word_counting(qa_records: Dict[str, QARecord]) -> int:
        word_cnt = 0
        for qa in qa_records.values():
            word_cnt += len(str(qa.question)) + len(str(qa.answer))
        return word_cnt

    @property
    def length(self):
        return len(self.qa_records)

    def __iter__(self):
        self.current_conversation_index = 0
        self.current_qa_record_id = self.conversation_start_id[0]
        return self

    def __next__(self) -> QARecord:
        # 每次迭代时，只输出一条QARecord消息，
        # 第一次迭代的时候，输出第一个conversation里面的第一条消息
        # 下次迭代时，输出第二条消息
        # 如果当前conversation已经迭代完毕（即successor_uid为None），则输出第二个conversation里面的第一条消息
        # 直到所有的conversation输出完毕
        if self.current_conversation_index >= len(self.qa_records):
            raise StopIteration

        qa_record = self.qa_records[self.current_qa_record_id]

        if qa_record.successor_uid is None:
            self.current_conversation_index += 1
            if self.current_conversation_index < len(self.conversation_start_id):
                self.current_qa_record_id = self.conversation_start_id[
                    self.current_conversation_index
                ]
        else:
            self.current_qa_record_id = qa_record.successor_uid
        return qa_record

    @staticmethod
    def edit(uid, conf: DatasetTyping) -> ReturnCode:  # 编辑数据集信息，返回状态码
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

    @classmethod
    def create_from_file(cls, file_path: str) -> Union[DatasetTyping, str]:
        dataset = cls(file=file_path)
        return dataset
