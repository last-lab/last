from typing import List, Optional, Type

from fastapi import Depends, HTTPException
from fastapi.params import Path
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from tortoise import Tortoise

from fastapi_admin import enums
from fastapi_admin.exceptions import InvalidResource
from fastapi_admin.providers.admin_log import AdminLogProvider
from fastapi_admin.providers.permission import PermissionProvider
from fastapi_admin.resources import Dropdown, Link, Model, Resource


def get_model(resource: Optional[str] = Path(...)):
    if not resource:
        return
    for app, models in Tortoise.apps.items():
        models = {key.lower(): val for key, val in models.items()}
        model = models.get(resource)
        if model:
            return model


def get_redis(request: Request):
    return request.app.redis


def get_current_admin(request: Request):
    admin = request.state.admin
    if not admin:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    return admin


class PermissionsChecker:
    def __init__(self, permission: enums.Permission):
        self.permission = permission

    async def __call__(
        self,
        request: Request,
        resource: str = Path(...),
        admin=Depends(get_current_admin),
    ):
        permission_provider = request.app.permission_provider
        if not permission_provider:
            return
        await admin.fetch_related("roles")
        has_permission = await permission_provider.check(admin, resource, self.permission)
        if not has_permission:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN)


read_checker = PermissionsChecker(enums.Permission.read)
create_checker = PermissionsChecker(enums.Permission.create)
update_checker = PermissionsChecker(enums.Permission.update)
delete_checker = PermissionsChecker(enums.Permission.delete)


async def _get_resources(
    resources: List[Type[Resource]], admin, permission_provider: PermissionProvider
):
    ret = []
    for resource in resources:
        item = {
            "icon": resource.icon,
            "label": resource.label,
        }
        if issubclass(resource, Link):
            if permission_provider and not await permission_provider.check(
                admin, resource.label, enums.Permission.read
            ):
                continue
            item["type"] = "link"
            item["url"] = resource.url
            item["target"] = resource.target
        elif issubclass(resource, Model):
            r = resource.model.__name__.lower()
            if permission_provider and not await permission_provider.check(
                admin, r, enums.Permission.read
            ):
                continue
            item["type"] = "model"
            item["model"] = r
        elif issubclass(resource, Dropdown):
            rs = await _get_resources(resource.resources, admin, permission_provider)
            if not rs:
                continue
            item["type"] = "dropdown"
            item["resources"] = rs
            item["expand"] = resource.expand
        else:
            raise InvalidResource("Should be subclass of Resource")
        ret.append(item)
    return ret


async def get_resources(request: Request, admin=Depends(get_current_admin)) -> List[dict]:
    resources = request.app.resources
    await admin.fetch_related("roles")
    return await _get_resources(resources, admin, request.app.permission_provider)


async def get_model_resource(
    request: Request,
    model=Depends(get_model),
    resource: str = Path(...),
    admin=Depends(get_current_admin),
):
    model_resource = request.app.get_model_resource(model)  # type:Model
    if not model_resource:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    permission_provider = request.app.permission_provider
    actions = await model_resource.get_actions(request)
    bulk_actions = await model_resource.get_bulk_actions(request)
    toolbar_actions = await model_resource.get_toolbar_actions(request)
    if permission_provider and not await permission_provider.check(
        admin, resource, enums.Permission.create
    ):
        create_action = list(
            filter(lambda x: x.name in [enums.Permission.create, "import"], toolbar_actions)
        )
        if create_action:
            toolbar_actions.remove(create_action[0])
    if permission_provider and not await permission_provider.check(
        admin, resource, enums.Permission.update
    ):
        update_action = list(filter(lambda x: x.name == enums.Permission.update, actions))
        if update_action:
            actions.remove(update_action[0])
    if permission_provider and not await permission_provider.check(
        admin, resource, enums.Permission.delete
    ):
        delete_action = list(filter(lambda x: x.name == enums.Permission.delete, actions))
        if delete_action:
            actions.remove(delete_action[0])
        delete_bulk_action = list(filter(lambda x: x.name == enums.Permission.delete, bulk_actions))
        if delete_bulk_action:
            bulk_actions.remove(delete_bulk_action[0])
    setattr(model_resource, "actions", actions)
    setattr(model_resource, "bulk_actions", bulk_actions)
    setattr(model_resource, "toolbar_actions", toolbar_actions)
    return model_resource


class AdminLog:
    def __init__(self, action: str):
        self.action = action

    async def __call__(
        self,
        request: Request,
        resource: str = Path(...),
        admin=Depends(get_current_admin),
    ):
        yield
        admin_log_provider = request.app.admin_log_provider  # type:AdminLogProvider
        if admin_log_provider:
            await admin_log_provider.log(request, resource, admin, self.action)


admin_log_create = AdminLog(action=enums.Action.create.value)
admin_log_update = AdminLog(action=enums.Action.update.value)
admin_log_delete = AdminLog(action=enums.Action.delete.value)
