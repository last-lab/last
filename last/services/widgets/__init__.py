from typing import Any

from starlette.requests import Request
from starlette.templating import Jinja2Templates

from last.services.template import templates as t


class Widget:
    templates: Jinja2Templates = t
    template: str = ""

    def __init__(self, **context):
        """
        All context will pass to template render if template is not empty.
        :param context:
        """
        self.context = context

    async def render(self, request: Request, value: Any):
        if value is None:
            value = ""
        if not self.template:
            return value
        return self.templates.get_template(self.template).render(value=value, **self.context)
