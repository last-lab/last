import datetime
from typing import Any

from starlette.requests import Request
from tortoise.queryset import QuerySet

from dashboard.biz_models import Risk
from last.services.widgets.filters import Filter, Search


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


class SearchFilter(Search):
    async def get_queryset(self, request: Request, value: Any, qs: QuerySet):
        value = await self.parse_value(request, value)
        first_risk = await Risk.get_or_none(risk_name=value).values()
        if first_risk is None:
            filters = {self.context.get("name"): ""}
        else:
            filters = {self.context.get("name"): first_risk["risk_id"]}
        return qs.filter(**filters)
