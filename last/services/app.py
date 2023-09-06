from typing import Dict, List, Optional, Type

from fastapi import FastAPI
from redis.asyncio import Redis
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise.models import Model

from . import enums, i18n, middlewares, template
from .providers import Provider
from .resources import Dropdown
from .resources import Model as ModelResource
from .resources import Resource
from .routes import router


class FastAPIAdmin(FastAPI):
    logo_url: Optional[str]
    admin_path: str
    maintenance: bool = False
    resources: List[Type[Resource]] = []
    model_resources: Dict[Type[Model], Type[Resource]] = {}
    redis: Redis
    language_switch: bool = True
    favicon_url: Optional[str] = None
    default_layout: enums.Layout = enums.Layout.layout
    site_title: Optional[str]

    async def configure(
        self,
        redis: Redis,
        logo_url: Optional[str] = None,
        default_locale: str = "en_US",
        language_switch: bool = True,
        admin_path: str = "/admin",
        template_folders: Optional[List[str]] = None,
        maintenance: bool = False,
        providers: Optional[List[Provider]] = None,
        favicon_url: Optional[str] = None,
        site_title: Optional[str] = None,
        default_layout: enums.Layout = enums.Layout.layout,
    ):
        """
        Config FastAdmin
        :param redis: Redis instance of aioredis
        :param maintenance: If set True,all request will redirect to maintenance page
        :param logo_url:
        :param default_locale:
        :param admin_path:
        :param template_folders: Template folders, if same as builtin, then will cover that
        :param language_switch:
        :param providers:
        :param favicon_url:
        :param default_layout:
        :param site_title:
        :return:
        """
        self.redis = redis
        i18n.set_locale(default_locale)
        self.admin_path = admin_path
        self.logo_url = logo_url
        self.maintenance = maintenance
        self.language_switch = language_switch
        self.default_layout = default_layout
        self.favicon_url = favicon_url
        self.site_title = site_title
        if template_folders:
            template.add_template_folder(*template_folders)
        await self._register_providers(providers)

    async def _register_providers(self, providers: Optional[List[Provider]] = None):
        for p in providers or []:
            await p.register(self)

    def register_resources(self, *resource: Type[Resource]):
        for r in resource:
            self.register(r)

    def _set_model_resource(self, resource: Type[Resource]):
        if issubclass(resource, ModelResource):
            self.model_resources[resource.model] = resource
        elif issubclass(resource, Dropdown):
            for r in resource.resources:
                self._set_model_resource(r)

    def register(self, resource: Type[Resource]):
        self._set_model_resource(resource)
        self.resources.append(resource)

    def get_model_resource(self, model: Type[Model]):
        r = self.model_resources.get(model)
        return r() if r else None


app = FastAPIAdmin(
    title="FastAdmin",
    description="A fast admin dashboard based on fastapi and tortoise-orm with tabler ui.",
)
app.add_middleware(middlewares.MaintenanceMiddleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=middlewares.language_processor)
app.add_middleware(BaseHTTPMiddleware, dispatch=middlewares.layout_processor)
app.include_router(router)

