"""
类型转换类
"""
import json
from typing import Union

from pydantic.dataclasses import dataclass


class DataSetTool:

    @classmethod
    def ds_model_to_schema(cls, datasets):
        dataset_schemas = []

        for item in datasets:
            risk_group_dict = {}
            if item.dimensions is not None:
                risk_group_dict = cls.process_dimensions(item.dimensions)
            dataset_schema = DataSetSchema(id=item.id, name=item.name, risk_type=risk_group_dict.get(1, None),
                                           risk_second_type=risk_group_dict.get(2, None),
                                           risk_third_type=risk_group_dict.get(3, None))
            dataset_schemas.append(dataset_schema)
        return dataset_schemas

    @classmethod
    def process_dimensions(cls, dimensions):
        """
        功能：根据json类型的dimensions转换为分组的风险级别名称
        输入：[{"level":1,"name":"国家安全","description":""},{"level":2,"name":"颠覆政权","description":""},{"level":3,"name":"敏感信息","description":""}]
        输出：{"1": "国家安全","2":"颠覆政权", "3": "敏感信息"}
        """
        risk_group_dict = {}
        risk_dict_list = json.loads(dimensions)
        for item in risk_dict_list:
            level = item['level']
            name = item['name']
            if level in risk_group_dict:
                risk_group_dict[level] += f", {name}"
            else:
                risk_group_dict[level] = name
        return risk_group_dict


@dataclass
class DataSetSchema:
    """
    评测方案管理依赖的数据集数据
    """
    id: int
    name: Union[str, None] = None
    risk_type: Union[str, None] = None
    risk_second_type: Union[str, None] = None
    risk_third_type: Union[str, None] = None
