"""
类型转换类
"""
from typing import List, Optional, Union

from pydantic.dataclasses import dataclass

from dashboard.biz_models import Risk


@dataclass
class DataSetEvalPlanSchema:
    """
    评测方案管理依赖的数据集结构
    """

    id: int
    name: Union[str, None] = None
    risk_type: Union[str, None] = None
    risk_second_type: Union[str, None] = None
    risk_third_type: Union[str, None] = None


@dataclass
class DataSetEvalModelSchema:
    """
    模型评测依赖的数据集数据结构
    """

    dataset_names: Optional[List[str]] = None
    risk_detail: Optional[List[List]] = None


@dataclass
class RiskSchema:
    risk_id: str
    risk_level: int
    risk_name: str
    parent_risk_id: Optional[str] = None
    children: Optional[List[dict]] = None


class DataSetTool:
    @classmethod
    async def ds_model_to_eval_model_schema(cls, datasets) -> DataSetEvalModelSchema:
        """
        功能：根据dataset列表转为模型评测需要的数据结构
        输入参数：
        datasets：[{"id":1, "name":"ds1","focused_risks":"1,2,3", ...}]
        输出参数：
        {"dataset_names": "ds1, ds2","risk_detail":[{"name": 一级1, "children":[{"name": "二级1", "children": [{"name":"三级1"}]}]}]}
        """
        dataset_names = []
        risk_detail = []
        for item in datasets:
            dataset_names.append(item.name)
            if not item.focused_risks:
                continue
            risk_list = await Risk.filter(risk_id__in=eval(item.focused_risks))
            risk_schemas = list(
                map(
                    lambda risk: RiskSchema(
                        risk_id=risk.risk_id,
                        risk_level=risk.risk_level,
                        risk_name=risk.risk_name,
                        parent_risk_id=risk.parent_risk_id,
                    ),
                    risk_list,
                )
            )

            risk_detail.append(cls.build_risk_tree(risk_schemas))
        return DataSetEvalModelSchema(dataset_names=dataset_names, risk_detail=risk_detail)

    @classmethod
    async def ds_model_to_eval_plan_schema(cls, datasets):
        """
        功能：根据dataset列表转为评测方案需要的数据结构
        输入参数：
        datasets：[{"id":1, "name":"ds1","focused_risks":"1,2,3", ...}]
        输出参数：
        [{"id": 1,"name":"ds1", "risk_type": "国家安全", "risk_second_type":"二级风险", "risk_third_type": "三级风险"}]
        """
        dataset_schemas = []

        for item in datasets:
            risk_group_dict = {}
            if item.focused_risks is not None:
                risk_group_dict = await cls.process_focused_risks_for_eval_plan(item.focused_risks)
            dataset_schema = DataSetEvalPlanSchema(
                id=item.id,
                name=item.name,
                risk_type=risk_group_dict.get(1, None),
                risk_second_type=risk_group_dict.get(2, None),
                risk_third_type=risk_group_dict.get(3, None),
            )
            dataset_schemas.append(dataset_schema)
        return dataset_schemas

    @classmethod
    async def process_focused_risks_for_eval_plan(cls, focused_risks):
        """
        功能：根据json类型的dimensions转换为分组的风险级别名称
        输入参数：
        focused_risks："1,2,3"
        输出参数：
        {"1": "国家安全","2":"颠覆政权", "3": "敏感信息"}
        """
        risk_group_dict = {}
        risk_list = await Risk.filter(risk_id__in=eval(focused_risks))
        for item in risk_list:
            level = item.risk_level
            name = item.risk_name
            if level in risk_group_dict:
                risk_group_dict[level] += f", {name}"
            else:
                risk_group_dict[level] = name

        return risk_group_dict

    @classmethod
    def build_risk_tree(cls, risk_schemas, parent_risk_id=None):
        risk_tree = []
        for item in risk_schemas:
            if item.parent_risk_id == parent_risk_id:
                children = cls.build_risk_tree(risk_schemas, item.risk_id)
                if children:
                    item.children = children
                risk_tree.append({"name": item.risk_name, "children": children})
        return risk_tree
