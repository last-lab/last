from typing import List, Dict, Union, Optional, TypeVar
from pydantic import BaseModel
from enum import Enum

from .base import Record, Statistics, BaseManager
from .public import RiskDimension, RelatedRiskDimensions, ReturnCode
from .dataset import Dataset, Message


T = TypeVar('T', bound='Plan')

class EvaluationType(str, Enum):
    auto_exact_match = "auto_exact_match"
    auto_similarity_match = "auto_similarity_match"
    auto_ai_critique = "auto_ai_critique"
    human_a_b_testing = "human_a_b_testing"
    human_scoring = "human_scoring"
    human_ranking = "human_ranking"
    human_boxing = "human_boxing"    



class Plan(Record, BaseManager):
    """
    评测方案信息
    """

    name: str
    eval_type: EvaluationType # 系统评分、人工评分
    dimensions: Optional[Dict[RiskDimension.name, str]]  # 填写各个一级风险维度的占比%
    datasets: List[Dataset]
    focused_risk: Optional[RelatedRiskDimensions]  # 新建时不填写
    current_index: int

    def __post_init__(self):
        # 将新建的Plan对象同步到DB中
        Plan.new(self.url)

    @staticmethod
    def edit(id, conf: T) -> ReturnCode:  # 编辑评测方案，返回状态码
        pass

    @staticmethod
    def fork(id) -> str:  # 返回新的方案id
        pass



    def __iter__(self):
        return self

    def __next__(self) -> Message:
        pass
        # if self.current_index >= len(self.datasets):
        #     raise StopIteration
        # dataset = self.datasets[self.current_index]
        # self.current_index += 1
        # yield dataset # 



class RiskDataDistribution(Record):
    num_QA: int
    percent: str
    weight: str

    def __str__(self):
        return f"{self.num_QA}条问答 占比{self.percent} 权重{self.weight}"
