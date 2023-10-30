import json
from typing import Type

from starlette.datastructures import UploadFile
from starlette.requests import Request
from tortoise import Model

from last.services.models import AbstractAdmin, AbstractLog
from last.services.providers import Provider
from last.services.utils import get_client_ip


class AdminLogProvider(Provider):
    name = "admin_log_provider"

    def __init__(self, log_model: Type[Model] = AbstractLog):
        self.log_model = log_model

    async def log(self, request: Request, resource: str, admin: AbstractAdmin, action: str):
        pk = request.path_params.get("pk")
        content = {"content": {}}
        if pk:
            content["pk"] = pk
        else:
            content["pk"] = getattr(request.state, "pk", None)
        if request.method in ["POST", "PUT"]:
            body = dict(await request.form())
            for k, v in body.items():
                if k in ["save", "save_and_return", "save_and_add_another"]:
                    continue
                if isinstance(v, UploadFile):
                    content["content"][k] = v.filename
                else:
                    content["content"][k] = v
        await self.log_model.create(
            ip=get_client_ip(request),
            admin=admin,
            action=action,
            resource=resource,
            content=json.dumps(content),
        )
