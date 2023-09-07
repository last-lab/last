from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel

from .base import Record, Statistics
from .public import RiskDimension, RelatedRiskDimensions
from .dataset import Dataset

@dataclass
class Task(Record):
    """
    方案信息
    """
    name: str
    level_1_dimensions: Dict[RiskDimension.name, str] 
    dataset_name: List[Dataset.name] 
    focused_risk: RelatedRiskDimensions

@dataclass
class RiskDataDistribution(Record):
    num_QA: int
    percent: str
    weight: str
    def __str__(self):
        return f"{self.num_QA}条问答 占比{self.percent} 权重{self.weight}"



class TaskManager(BaseManager):
    @staticmethod 
    def edit(orm: ORMModel, id, conf: Task) -> ReturnCode: # 编辑评测方案，返回状态码
        pass

    @staticmethod
    def fork(id) -> str: #返回新的方案id
        pass

