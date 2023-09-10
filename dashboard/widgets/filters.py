import datetime
from typing import Any

from starlette.requests import Request
from tortoise.queryset import QuerySet

from last.services.widgets.filters import Filter


class DueSoon(Filter):
    async def get_options(self):
        ret = [("Yes", "1"), ("No", "0"), ("Invalid", "-1")]
        if self.context.get("null"):
            ret = [("", "")] + ret
        return ret

    async def get_queryset(self, request: Request, value: Any, qs: QuerySet):
        today = datetime.date.today()
        day = today + datetime.timedelta(days=7)
        if value == "1":
            qs = qs.filter(invalid_date__range=(today, day))
        elif value == "0":
            qs = qs.filter(invalid_date__gt=day)
        elif value == "-1":
            qs = qs.filter(invalid_date__lt=today)
        return qs
