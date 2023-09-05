import typing
from typing import Type

from tortoise.transactions import in_transaction

from fastapi_admin import enums
from fastapi_admin.exceptions import ConfigurationError
from fastapi_admin.models import AbstractAdmin, AbstractPermission, AbstractResource
from fastapi_admin.providers import Provider
from fastapi_admin.resources import Dropdown, Link, Model, Resource

if typing.TYPE_CHECKING:
    from fastapi_admin.app import FastAPIAdmin


class PermissionProvider(Provider):
    name = "permission_provider"

    def __init__(
        self,
        admin_model: Type[AbstractAdmin],
        resource_model: Type[AbstractResource],
        permission_model: Type[AbstractPermission],
    ):
        self.resource_model = resource_model
        self.permission_model = permission_model
        self.admin_model = admin_model

    async def register(self, app: "FastAPIAdmin"):
        await super(PermissionProvider, self).register(app)
        admin_model = self.admin_model
        fields = admin_model._meta.fields
        if "is_superuser" not in fields or "is_active" not in fields:
            raise ConfigurationError(
                f"`is_superuser` and `is_active` must add in admin_model `{admin_model}` as BooleanField"
            )
        async with in_transaction() as conn:
            await self.fill_permission_data(conn, app.resources)

    async def fill_permission_data(self, conn, resources: typing.List[Type[Resource]]):
        resource_model = self.resource_model
        permission_model = self.permission_model
        for r in resources:
            if issubclass(r, Dropdown):
                await self.fill_permission_data(conn, r.resources)
            else:
                await resource_model.get_or_create(label=r.label, using_db=conn)
                if issubclass(r, Link):
                    await permission_model.get_or_create(
                        resource=r.label, label=r.label, using_db=conn
                    )
                elif issubclass(r, Model):
                    for p in enums.Permission:
                        await permission_model.get_or_create(
                            resource=r.model.__name__,
                            label=r.label,
                            permission=p,
                            using_db=conn,
                        )

    @classmethod
    async def check(cls, admin: AbstractAdmin, resource: str, permission: enums.Permission) -> bool:
        if admin.is_superuser:
            return True
        if not admin.is_active:
            return False
        has_permission = False
        for role in admin.roles:
            admin.role_name = role.label
            if await role.permissions.filter(resource=resource, permission=permission).exists():
                has_permission = True
                break
        return has_permission
