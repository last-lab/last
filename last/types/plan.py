from typing import List, Dict, Union, Optional, TypeVar, Any
from enum import Enum
from dataclasses import dataclass
from .base import Record, Statistics, BaseManager
from .public import RiskDimension, RelatedRiskDimensions, ReturnCode
from .dataset import Dataset, Message
from pydantic import BaseModel, Field

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
    dimensions: Optional[Dict[str, str]]  # 填写各个一级风险维度的占比%
    datasets: List[Dataset]
    focused_risk: Optional[RelatedRiskDimensions]  # 新建时不填写
    current_dataset_index: Optional[int] = Field(init=False)
    current_dataset_iter: Optional[Any] = Field(init=False)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.__post_init__()  # 调用 __post_init__ 方法

    def __iter__(self):
        self.current_dataset_index = 0
        self.current_dataset_iter = iter(self.datasets[self.current_dataset_index])
        return self

    def __next__(self) -> Message:
        try:
            return next(self.current_dataset_iter)
        except StopIteration:
            self.current_dataset_index += 1
            if self.current_dataset_index < len(self.datasets):
                self.current_dataset_iter = iter(self.datasets[self.current_dataset_index])
                return next(self.current_dataset_iter)
            else:
                raise

    # def __post_init__(self):
    #     # 将新建的Plan对象同步到DB中
    #     Plan.new(self.url)

    @staticmethod
    def edit(id, conf: T) -> ReturnCode:  # 编辑评测方案，返回状态码
        pass

    @staticmethod
    def fork(id) -> str:  # 返回新的方案id
        pass


class RiskDataDistribution(Record):
    num_QA: int
    percent: str
    weight: str

    def __str__(self):
        return f"{self.num_QA}条问答 占比{self.percent} 权重{self.weight}"
