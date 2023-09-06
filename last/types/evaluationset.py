from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel

@dataclass
class EvaluationSetDimension:
    level: int
    name: str
    description: str
@dataclass
class EvaluationSet:
    """ Summary
    Description

    doctest
    """
    id: str # UUID-4
    name: str
    description: str
    dimensions: List[EvaluationSetDimension]
    url: str
    created_at: str
    updated_at: str
    used_by: List[str]
    permissions: List[str]
    statistics: Dict[str, Union[int, float]]

def create_model(e_set:EvaluationSet): -> ORMModel:
    pass

def create_dataloader(): -> torch.DataLoader:
    pass

