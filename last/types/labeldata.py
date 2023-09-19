from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional, Dict, Any
from .base import Record
from .dataset import Message
from .annotation import Annotations
from .public import UserInfo, StateCode, ReturnCode, DateString


@dataclass
class AnnotationTaskInfo(Record):
    # 任务信息
    task_id: str
    task_type: str  # 数据标注、审计标注
    data_type: Optional[str]  # 数据类型，如文本、图像、音频、视频等，暂时只有文本
    annotation_method: str  # 标注方式 0-1标注，box标注，rank标注等
    publish_time: DateString  # Message/Record的创建时间
    state: StateCode  # 任务是否被完成


# 标注任务的输入数据格式
class AnnotationTaskInput(AnnotationTaskInfo):
    annotation_content: Optional[Annotations]  # 可能是对已有的标注编辑、审阅，所以可能需要传入现有的annotation


# 数据标注任务管理页面的数据格式 @亮亮 参考这里
@dataclass
class AnnotationTask(AnnotationTaskInfo):
    # 调用label studio进行标注
    def annotate(task_id: str) -> ReturnCode:
        pass

    # 审阅标注
    def review(task_id: str) -> ReturnCode:
        pass

    # 查看结果
    def view_results(task_id: str) -> ReturnCode:
        pass

    # 导出数据
    def export_data(task_id: str) -> ReturnCode:
        pass


# 标注任务的数据输出格式
class AnnotationTaskOutput(AnnotationTaskInfo, Annotations):
    # TODO 标注任务->数据库中的操作
    def create(self) -> ReturnCode:
        pass

    def update(self) -> ReturnCode:
        pass

    def delete(self) -> ReturnCode:
        pass

    def get(self) -> ReturnCode:
        pass
