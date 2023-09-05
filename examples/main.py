import os

import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI
from rearq.server.app import app as rearq_server
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from tortoise import Tortoise

from examples import settings
from examples.constants import BASE_DIR
from examples.models import Admin, Log, Permission, Resource
from examples.providers import (
    GitHubProvider,
    GoogleProvider,
    LoginProvider,
    import_export_provider,
)
from examples.tasks import rearq
from fastapi_admin import enums, middlewares
from fastapi_admin.app import app as admin_app
from fastapi_admin.exceptions import (
    forbidden_error_exception,
    not_found_error_exception,
    server_error_exception,
    unauthorized_error_exception,
)
from fastapi_admin.providers.admin_log import AdminLogProvider
from fastapi_admin.providers.notification import NotificationProvider
from fastapi_admin.providers.permission import PermissionProvider
from fastapi_admin.providers.search import SearchProvider


def create_app():
    app = FastAPI()
    app.mount(
        "/static",
        StaticFiles(directory=os.path.join(BASE_DIR, "static")),
        name="static",
    )
    app.mount("/rearq", rearq_server)
    rearq_server.set_rearq(rearq)

    @app.get("/")
    async def index():
        return RedirectResponse(url="/admin")

    admin_app.add_middleware(
        middlewares.LoginPasswordMaxTryMiddleware, max_times=3, after_seconds=900
    )

    admin_app.add_exception_handler(
        HTTP_500_INTERNAL_SERVER_ERROR, server_error_exception
    )
    admin_app.add_exception_handler(HTTP_404_NOT_FOUND, not_found_error_exception)
    admin_app.add_exception_handler(HTTP_403_FORBIDDEN, forbidden_error_exception)
    admin_app.add_exception_handler(HTTP_401_UNAUTHORIZED, unauthorized_error_exception)

    app.mount("/admin", admin_app)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    @app.on_event("startup")
    async def startup():
        await rearq.startup()
        await Tortoise.init(config=settings.TORTOISE_ORM)
        await Tortoise.generate_schemas()
        r = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            encoding="utf8",
        )
        await admin_app.configure(
            logo_url="https://preview.tabler.io/static/logo-white.svg",
            favicon_url="https://raw.githubusercontent.com/fastapi-admin/fastapi-admin/dev/images/favicon.png",
            template_folders=[os.path.join(BASE_DIR, "templates")],
            providers=[
                LoginProvider(
                    admin_model=Admin,
                    login_logo_url="https://preview.tabler.io/static/logo.svg",
                ),
                PermissionProvider(
                    Admin,
                    Resource,
                    Permission,
                ),
                AdminLogProvider(Log),
                SearchProvider(),
                NotificationProvider(),
                GitHubProvider(
                    Admin, settings.GITHUB_CLIENT_ID, settings.GITHUB_CLIENT_SECRET
                ),
                GoogleProvider(
                    Admin,
                    settings.GOOGLE_CLIENT_ID,
                    settings.GOOGLE_CLIENT_SECRET,
                    redirect_uri="https://fastapi-admin-pro.long2ice.io/admin/oauth2/google_oauth2_provider",
                ),
                import_export_provider,
            ],  # type: ignore
            redis=r,
            default_layout=enums.Layout.layout,
        )
        await rearq_server.start_worker(with_timer=True)

    return app


app_ = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app_", reload=True)
