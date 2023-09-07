from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel

from .base import Record, Statistics
from .public import RiskDimension

@dataclass
class EvaluationSetDimension:
    level: int
    name: str
    description: str

@dataclass
class EvaluationSet(Record):
    name: str
    dimensions: List[RiskDimension]
    url: str
    used_by: List[str]


def create_dataloader() -> torch.DataLoader:
    pass

