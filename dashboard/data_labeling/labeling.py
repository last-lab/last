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

from starlette.requests import Request
from typing import List

class LabelPageModel(Model):
    async def get_toolbar_actions(self, request: Request) -> List[ToolbarAction]:
        return []
