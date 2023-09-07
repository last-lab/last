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
    def edit(orm: ORMModel, id, conf: DatasetInfo) -> ReturnCode: # 编辑评测方案，返回状态码
        pass





def create_dataloader() -> torch.DataLoader:
    pass

