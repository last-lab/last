from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import RedirectResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.types import ASGIApp, Receive, Scope, Send

from last.services import constants, i18n, utils
from last.services.i18n import _
from last.services.template import set_global_env, templates


async def language_processor(request: Request, call_next: Callable):
    locale = request.query_params.get("language")
    if not locale:
        locale = request.cookies.get("language")
        if not locale:
            accept_language = request.headers.get("Accept-Language")
            if accept_language:
                locale = accept_language.split(",")[0].replace("-", "_")
            else:
                locale = None
    i18n.set_locale(locale)
    response = await call_next(request)
    if locale:
        response.set_cookie(key="language", value=locale)
    return response


async def layout_processor(request: Request, call_next: Callable):
    layout = request.cookies.get("layout")
    if layout:
        set_global_env("layout", layout)
    else:
        set_global_env("layout", str(request.app.default_layout))
    response = await call_next(request)
    return response


class MaintenanceMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        app = scope["app"]
        if scope["path"] != "/maintenance" and app.maintenance:
            response = RedirectResponse(app.admin_path + "/maintenance")
            await response(scope, receive, send)
        else:
            await self.app(scope, receive, send)


class LoginPasswordMaxTryMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, app: ASGIApp, max_times: int = 3, after_seconds: int = 900
    ) -> None:
        super().__init__(app)
        self.max_times = max_times
        self.after_seconds = after_seconds

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path = request.scope["path"]
        redis = request.app.redis
        ip = utils.get_client_ip(request)
        is_login_path = (
            path == request.app.login_provider.login_path and request.method == "POST"
        )
        key = constants.LOGIN_ERROR_TIMES.format(ip=ip)
        if is_login_path:
            ttl = await redis.ttl(key)
            if ttl == -1:
                ttl = self.after_seconds
                await redis.expire(key, self.after_seconds)
            times = await redis.get(key) or 0
            if int(times) >= self.max_times:
                return templates.TemplateResponse(
                    request.app.login_provider.template,
                    context={
                        "request": request,
                        "error": _("You can only try after %(seconds)s seconds")
                        % dict(seconds=ttl),
                    },
                )
        response = await call_next(request)
        if is_login_path and response.status_code == HTTP_401_UNAUTHORIZED:
            times = await redis.incr(key)
            return templates.TemplateResponse(
                request.app.login_provider.template,
                context={
                    "request": request,
                    "error": _(
                        "Login failed %(times)s times, you can try %(rest_times)s more times"
                    )
                    % dict(times=times, rest_times=self.max_times - times),
                },
            )
        return response
