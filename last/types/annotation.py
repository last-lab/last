from dataclasses import dataclass
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
from .base import Record


# 定义单个标注结果的数据结构，也就是存入annotation数据库的数据结构
@dataclass
class AnnotationResult(Record):
    annotation_task_id: str  # 任务ID
    value: Dict  # 标注的值，可以使用AnnotationValue，或者直接打包前端返回的annotation结果。
    data_type: str  # 标注对象的数据类型，text, image, video
    annotation_target: str  # 标注的目的，sentiment, answer
    annotation_type: str  # 标注方法的类型 0-1标注，box标注，rank标注等
    origin: str  # 标注的来源（手动或自动）
    complete_time: Optional[float]  # 完成标注所需的时间（秒），可选

    

# 暂时不需要用到
# 定义标注结果中的值结构，参考label studio
@dataclass
class AnnotationValue(BaseModel):
    start: Optional[int] = None  # 起始位置，可选
    end: Optional[int] = None  # 结束位置，可选
    text: Optional[str] = None  # 文本内容，可选
    choices: Optional[List[str]] = None  # 可选项列表，可选
    labels: Optional[List[str]] = None  # 标签列表，可选
    taxonomy: Optional[List[List[str]]] = None  # 分类学信息，可选
