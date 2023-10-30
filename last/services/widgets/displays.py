import json
from datetime import date, datetime
from typing import Optional

import pendulum
from starlette.requests import Request

from last.services import constants
from last.services.widgets import Widget


class Display(Widget):
    """
    Parent class for all display widgets
    """


class DatetimeDisplay(Display):
    def __init__(self, format_: str = constants.DATETIME_FORMAT, **context):
        super().__init__(**context)
        self.format_ = format_

    async def render(self, request: Request, value: datetime):
        if isinstance(value, datetime):
            return await super(DatetimeDisplay, self).render(
                request,
                pendulum.instance(value).format(self.format_) if value else None,
            )
        elif isinstance(value, date):
            return await super(DatetimeDisplay, self).render(
                request,
                pendulum.date(value.year, value.month, value.day).format(self.format_)
                if value
                else None,
            )


class DateDisplay(DatetimeDisplay):
    def __init__(self, format_: str = constants.DATE_FORMAT, **context):
        super().__init__(format_, **context)


class InputOnly(Display):
    """
    Only input without showing in display
    """


class Boolean(Display):
    template = "widgets/displays/boolean.html"


class Status(Display):
    template = "widgets/displays/status.html"


class Popover(Display):
    template = "widgets/displays/popover.html"


class Image(Display):
    template = "widgets/displays/image.html"

    def __init__(self, width: Optional[str] = None, height: Optional[str] = None, **context):
        super().__init__(width=width, height=height, **context)


class Json(Display):
    template = "widgets/displays/json.html"

    async def render(self, request: Request, value: dict):
        return await super(Json, self).render(request, json.dumps(value))


class Link(Display):
    template = "widgets/displays/link.html"

    def __init__(self, target: str = "_blank", **context):
        super().__init__(target=target, **context)
