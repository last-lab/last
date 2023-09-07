from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel

from .base import Record, Statistics
from .public import RiskDimension


@dataclass
class DatasetInfo(Record):
    name: str
    dimensions: List[RiskDimension]
    url: str
    used_by: Optional[List[str]]


class DatasetManager(BaseManager):
    @staticmethod 
    def edit(id, conf: DatasetInfo) -> ReturnCode: # 编辑评测方案，返回状态码
        pass

    @staticmethod 
    def upload(content) -> str: # 返回id  
        QA_url = get_url(content)
        dataset_info = DatasetInfo(name="xxx", dimensions="xxxx", url=QA_url)
        uid = DatasetManager.new(DatasetInfo)
        return uid

def create_dataloader() -> torch.DataLoader:
    pass

