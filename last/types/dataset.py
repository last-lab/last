from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel

from .base import Record, Statistics
from .public import RiskDimension



@dataclass
class Dataset(Record, BaseManager):
    name: str
    dimensions: List[RiskDimension]
    url: str
    used_by: Optional[List[str]]

    def __post_init__(self):
        # 将新建的Dataset对象同步到DB中
        Dataset.new(Dataset)

    @staticmethod
    def edit(id, conf: DatasetInfo) -> ReturnCode:  # 编辑评测方案，返回状态码
        pass

    @staticmethod
    def upload(content) -> str:  # 返回id
        QA_url = get_url(content)
        dataset_info = DatasetInfo(name="xxx", dimensions="xxxx", url=QA_url)
        uid = DatasetManager.new(DatasetInfo)
        return uid


def create_dataloader() -> torch.DataLoader:
    pass
