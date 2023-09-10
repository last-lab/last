from typing import List

from starlette.requests import Request

from last.services.resources import (
    Action,
    ComputeField,
    Dropdown,
    Field,
    Link,
    Model,
    ToolbarAction,
)

# 标注主页面打开，需要调用从mock_data_into_sqlite


class LabelPageModel(Model):
    async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
        return []
