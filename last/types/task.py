from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel

from .base import Record, Statistics
from .public import RiskDimension, RelatedRiskDimensions
from .evaluationset import EvaluationSet

@dataclass
class TaskDetail(Record):
    """
    方案信息
    """
    name: str
    level_1_dimensions: Dict[RiskDimension.name, ] 
    dataset_name: List[EvaluationSet.name] 
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
    def edit(orm: ORMModel, id, conf: TaskDetail) -> ReturnCode: # 编辑评测方案，返回状态码
        pass

    @staticmethod
    def fork(id) -> str: #返回新的方案id
        pass

