from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel

from .base import Record, Statistics
from .public import RiskDimension


@dataclass
class Dataset(Record):
    name: str
    dimensions: List[RiskDimension]
    url: str
    used_by: List[str]


def create_dataloader() -> torch.DataLoader:
    pass

