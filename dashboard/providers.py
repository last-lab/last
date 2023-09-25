from fastapi import Depends, Form
from redis.asyncio import Redis
from starlette.requests import Request
from tortoise import timezone

from dashboard.import_export import CategoryImportExport
from dashboard.models import Admin, Role
from last.services.depends import get_current_admin, get_redis, get_resources
from last.services.models import AbstractAdmin
from last.services.providers.import_export import ImportExportProvider
from last.services.providers.login import (
    GitHubOAuth2Provider,
    GoogleOAuth2Provider,
    SSOOAuth2Provider,
    UsernamePasswordProvider,
)


class LoginProvider(UsernamePasswordProvider):
    async def password(
        self,
        request: Request,
        old_password: str = Form(...),
        new_password: str = Form(...),
        re_new_password: str = Form(...),
        admin: AbstractAdmin = Depends(get_current_admin),
        resources=Depends(get_resources),
    ):
        return await self.logout(request)

    async def login(self, request: Request, redis: Redis = Depends(get_redis)):
        response = await super(LoginProvider, self).login(request, redis)
        admin = request.state.admin
        if admin:
            await Admin.filter(pk=admin.pk).update(last_login=timezone.now())
        return response


class OAuth2ProviderMixin:
    @classmethod
    async def after_admin_login(cls, admin: AbstractAdmin, created: bool):
        if created:
            role = await Role.filter(label="admin").first()
            if role:
                await role.admins.add(admin)
            else:
                general_role = await Role.filter(label="general").first()
                if general_role:
                    await general_role.admins.add(admin)
        await Admin.filter(pk=admin.pk).update(last_login=timezone.now())
        return admin


class GitHubProvider(GitHubOAuth2Provider, OAuth2ProviderMixin):
    async def get_admin(self, user_info: dict):
        username = user_info.get("login")
        avatar = user_info.get("avatar_url")
        email = user_info.get("email")
        admin, created = await Admin.update_or_create(
            email=email,
            defaults=dict(
                avatar=avatar,
                password="",
                username=username,
                channel="github",
                last_login=timezone.now(),
            ),
        )
        return await self.after_admin_login(admin, created)


class GoogleProvider(GoogleOAuth2Provider, OAuth2ProviderMixin):
    async def get_admin(self, user_info: dict):
        username = user_info.get("name")
        avatar = user_info.get("picture")
        email = user_info.get("email")
        admin, created = await Admin.update_or_create(
            email=email,
            defaults=dict(
                avatar=avatar,
                password="",
                username=username,
                channel="google",
                last_login=timezone.now(),
            ),
        )
        return await self.after_admin_login(admin, created)


class SSOProvider(SSOOAuth2Provider, OAuth2ProviderMixin):
    def get_authorize_url(self):
        return self.authorize_url + "?clientId=" + self.client_id + "&redirect=" + self.redirect_uri

    async def get_admin(self, user_info: dict):
        username = user_info.get("username")
        avatar = user_info.get("avatar")
        email = user_info.get("email")
        if not avatar:
            avatar = ""
        if not email:
            email = ""
        admin, created = await Admin.update_or_create(
            email=email,
            defaults=dict(
                avatar=avatar,
                password="",
                username=username,
                channel="sso",
                last_login=timezone.now(),
                is_superuser=False,
            ),
        )
        return await self.after_admin_login(admin, created)


import_export_provider = ImportExportProvider(import_export_resources=[CategoryImportExport])
