from dataclasses import dataclass
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union
from .base import Record
from .labeldata import TaskInfo


# 定义注解结果中的值结构
class _AnnotationValue(BaseModel):
    start: Optional[int] = None  # 起始位置，可选
    end: Optional[int] = None  # 结束位置，可选
    text: Optional[str] = None  # 文本内容，可选
    choices: Optional[List[str]] = None  # 可选项列表，可选
    labels: Optional[List[str]] = None  # 标签列表，可选
    taxonomy: Optional[List[List[str]]] = None  # 分类学信息，可选


# 定义单个注解结果的数据结构
class _AnnotationResult(BaseModel):
    value: _AnnotationValue  # 注解的值
    id: str  # 注解的唯一标识符
    from_name: str  # 注解来源名称
    to_name: str  # 注解目标名称
    type: str  # 注解类型
    origin: str  # 注解的来源（手动或自动）


# 定义注解的数据结构
class Annotations(BaseModel,Record):
    id: int  # 注解的ID
    completed_by: int  # 完成注解的用户ID
    result: List[_AnnotationResult]  # 注解结果列表
    was_cancelled: bool  # 注解是否被取消
    ground_truth: bool  # 是否为基准真值
    lead_time: Optional[float] = None  # 完成注解所需的时间（秒），可选


# 定义文本数据的数据结构
class Text(BaseModel):
    text: str  # 文本内容


# 定义元数据的数据结构
class Meta(BaseModel):
    pass  # 如果meta字段有具体的结构，请在这里添加


# 定义Label Studio JSON文件的数据结构
class LabelStudioJSON(BaseModel):
    task_id: TaskInfo.task_id  # 当前标注任务的task_id
    annotations: List[Annotations]  # 注解列表
    file_upload: str  # 上传的文件名
    data: Text  # 文本数据(根据label studio定义的)
    meta: Meta  # 元数据
    created_at: str  # 创建时间
    updated_at: str  # 更新时间
    inner_id: int  # 内部ID
    total_annotations: int  # 总注解数
    cancelled_annotations: int  # 被取消的注解数
    total_predictions: int  # 总预测数
    comment_count: int  # 评论数
    unresolved_comment_count: int  # 未解决的评论数
    last_comment_updated_at: Optional[str] = None  # 最后一个评论的更新时间，可选
    project: int  # 项目ID
    updated_by: int  # 最后更新的用户ID
    unique_id: Optional[str] = None  # 唯一标识符，可选


# 当前任务的请求数据结构
class CurrentTaskRequest(BaseModel):
    task_id: str  # 被点击的任务ID


# 当前任务的响应数据结构
class CurrentTaskResponse(BaseModel):  # 任务对应的文本内容
    data_type: dict  # 数据类型
    data: Text  # 数据内容
    label_type: dict  # 标签类型
    label: dict  # 标签内容
