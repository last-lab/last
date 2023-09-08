from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel
import contextlib

from .base import Record, Statistics
from .public import RiskDimension, RelatedRiskDimensions
from .dataset import DatasetInfo


@dataclass
class Task(Record, BaseManager):
    """
    评测方案信息
    """

    name: str
    dimensions: Optional[Dict[RiskDimension.name, str]]  # 填写各个一级风险维度的占比%
    datasets: List[DatasetInfo]
    focused_risk: Optional[RelatedRiskDimensions]  # 新建时不填写

    def __post_init__(self):
        # 将新建的Task对象同步到DB中
        Task.new(self.url)

    @staticmethod
    def edit(id, conf: Task) -> ReturnCode:  # 编辑评测方案，返回状态码
        pass

    @staticmethod
    def fork(id) -> str:  # 返回新的方案id
        pass


@dataclass
class RiskDataDistribution(Record):
    num_QA: int
    percent: str
    weight: str

    def __str__(self):
        return f"{self.num_QA}条问答 占比{self.percent} 权重{self.weight}"
