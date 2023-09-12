from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional, Dict, Any
from .base import Record
from .annotation import Annotations


@dataclass
class _LabelData(Record):
    data_type: str  # 可能是文本、图像、音频、视频等
    content: Any  # 这里可以是str、bytes等，具体取决于数据的类型


@dataclass
class _AnnotationMethod(BaseModel):
    pass


@dataclass
class _TaskInfo(BaseModel):
    task_id: str
    task_type: str  # 数据标注、审计标注
    publish_time: str
    status: str


# 数据标注任务的数据类
@dataclass
class AnnotationTask(_TaskInfo, _LabelData, Annotations):
    annotation_method: _AnnotationMethod

    # TODO 调用label studio
    def annotate(self):
        pass

    def review(task_id: str) -> Dict :
        pass

    def view_results(task_id: str) -> Dict:
        pass

    def export_data(task_id: str) -> Dict:
        pass


class AnnotationTaskInput(_LabelData):
    annotation_method: _AnnotationMethod
    annotation_content: Optional[Annotations]  # 可能是对已有的标注编辑、审阅


class AnnotationTaskOutput(_LabelData, Annotations):
    publish_time: str
    status: str
