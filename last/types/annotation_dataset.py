from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional, Dict, List
from .base import Record
from .public import StateCode



# 定义标注对象的数据的数据格式
@dataclass
class AnnotatedData(Record):
    annotated_data_id: str  # 任务ID
    anotated_data_type: str  # 标注对象的数据类型，text, image, video
    content: str  # 标注对象的内容
    
 
# 定义标注任务的数据结构
@dataclass
class AnnotationTask(Record):
    annotation_task_id: str  # 任务ID
    annotated_data_id: str # 标注对象的数据ID
    anotated_data_type: str  # 标注对象的数据类型，text, image, video
    annotation_task_type: str  # 数据标注、审计标注
    annotation_target: str  # 标注的目的，sentiment, answer
    annotation_types: List[str]  # 标注方法的类型 0-1标注，box标注，rank标注等
    label_contents: List[Dict]  # 标注需要的label内容
    state: StateCode


# 定义单个标注结果的数据结构
@dataclass
class AnnotationResult(Record):
    annotation_task_id: str  # 任务ID
    annotation_sub_task_id: str  # 子任务ID，也就是本条annotation的id
    annotation_type: str  # 标注方法的类型 0-1标注，box标注，rank标注等
    annotated_data_id: str  # 标注对象的数据ID
    value: Dict  # 标注的值，直接打包前端返回的annotation结果，格式参考AnnotationValue
    origin: str  # 标注的来源（手动或自动）
    complete_time: Optional[float]  # 完成标注所需的时间（秒），可选
    sub_task_state: StateCode
    # 在Record中的字段
    # creator: UserInfo  # 标记者的id
    # created_at: DateString
    # updated_at:  Optional[DateString]
    # permissions: PermissionLevel


