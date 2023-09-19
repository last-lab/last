from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional, Dict, List
from .base import Record
from .public import StateCode

# 定义标注对象的数据的数据结构
@dataclass
class AnnotatedData(Record):
    annotated_data_id: str  # 标注数据集的id
    anotated_data_types: Optional[List[str]]  # 标注数据集的数据类型，text, image, video
    content: str  # 标注对象的内容
    
 
# 定义标注任务的数据结构
@dataclass
class AnnotationTask(Record):
    annotation_task_id: str  # 任务ID
    annotated_data_id: str # 标注对象的数据ID
    anotated_data_types: Optional[List[str]]  # 标注数据集的数据类型，text, image, video。上传数据集时应有的字段
    annotation_task_type: str  # 数据标注、审计标注
    annotation_method: List[str]  # 标注方法的类型 0-1标注，box标注，rank标注等
    annotation_target: Optional[str]  # 标注的目的，sentiment, answer
    label_contents: Optional[List[Dict]]  # 标注需要的label内容，目前直接前端固化流程
    assigned_annotators: List[str]  # 分配给标注者的ID列表
    assigned_auditors: List[str]  # 分配给审计者的ID列表


# 定义标注结果的数据结构
@dataclass
class AnnotationResult(Record):
    annotation_task_id: str  # 任务ID
    annotation_value: Dict  # 结构体形式（底层为链表），直接打包前端返回的annotation结果。需要包括annotation_method, update_time, complete_time(完成标注所需的时间), annotation_origin(标注的来源（手动或自动）) 等字段
    sub_task_state: StateCode  # 标注任务是否完成
    # 在Record中的字段 
    # creator: UserInfo  # 标记者的id
    # created_at: DateString
    # updated_at:  Optional[DateString]
    # permissions: PermissionLevel


