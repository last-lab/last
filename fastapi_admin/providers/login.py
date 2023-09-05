import typing
import uuid
from typing import Optional, Type
from urllib.parse import urlencode

import httpx
from captcha.image import ImageCaptcha
from fastapi import Depends, Form
from pydantic import BaseModel
from redis.asyncio import Redis
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import RedirectResponse, StreamingResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_401_UNAUTHORIZED, HTTP_412_PRECONDITION_FAILED
from tortoise import signals

from fastapi_admin import constants, utils
from fastapi_admin.depends import get_current_admin, get_redis, get_resources
from fastapi_admin.exceptions import ConfigurationError
from fastapi_admin.i18n import _
from fastapi_admin.models import AbstractAdmin
from fastapi_admin.providers import Provider
from fastapi_admin.template import templates
from fastapi_admin.utils import check_password, hash_password

if typing.TYPE_CHECKING:
    from fastapi_admin.app import FastAPIAdmin


class GoogleRecaptcha(BaseModel):
    cdn_url: str = "https://www.google.com/recaptcha/api.js"
    verify_url: str = "https://www.google.com/recaptcha/api/siteverify"
    site_key: str
    secret: str


class UsernamePasswordProvider(Provider):
    name = "login_provider"

    def __init__(
        self,
        admin_model: Type[AbstractAdmin],
        enable_captcha: bool = False,
        google_recaptcha: Optional[GoogleRecaptcha] = None,
        login_path="/login",
        logout_path="/logout",
        template="providers/login/login.html",
        login_title="Login to your account",
        login_logo_url: str = None,
    ):
        self.login_path = login_path
        self.logout_path = logout_path
        self.template = template
        self.admin_model = admin_model
        self.enable_captcha = enable_captcha
        self.google_recaptcha = google_recaptcha
        self.login_title = login_title
        self.login_logo_url = login_logo_url

    async def login_view(
        self,
        request: Request,
    ):
        return templates.TemplateResponse(
            self.template,
            context={
                "request": request,
                "login_title": self.login_title,
                "login_logo_url": self.login_logo_url,
            },
        )

    async def register(self, app: "FastAPIAdmin"):
        await super(UsernamePasswordProvider, self).register(app)
        login_path = self.login_path
        app.get(login_path)(self.login_view)
        app.post(login_path)(self.login)
        app.get(self.logout_path)(self.logout)
        app.add_middleware(BaseHTTPMiddleware, dispatch=self.authenticate)
        if self.enable_captcha:
            app.get("/captcha")(self.captcha)
        app.get("/init")(self.init_view)
        app.post("/init")(self.init)
        app.get("/password")(self.password_view)
        app.post("/password")(self.password)
        signals.pre_save(self.admin_model)(self.pre_save_admin)

    async def pre_save_admin(self, _, instance: AbstractAdmin, using_db, update_fields):
        if instance.pk:
            db_obj = await instance.get(pk=instance.pk)
            if db_obj.password != instance.password:
                instance.password = hash_password(instance.password)
        else:
            instance.password = hash_password(instance.password)

    async def captcha(
        self,
        request: Request,
        width: int = 160,
        height: int = 60,
        redis: Redis = Depends(get_redis),
    ):
        if not self.enable_captcha:
            raise ConfigurationError("Should enable captcha first")
        captcha = ImageCaptcha(width=width, height=height)
        code = utils.generate_random_str(4)
        captcha_id = uuid.uuid4().hex
        captcha_key = constants.CAPTCHA_ID.format(captcha_id=captcha_id)
        image = captcha.generate(code)
        response = StreamingResponse(content=image, media_type="image/png")
        await redis.set(captcha_key, code, ex=60)
        response.set_cookie(
            "captcha_id",
            captcha_id,
            max_age=60,
            path=request.app.admin_path,
            httponly=True,
        )
        return response

    async def login(self, request: Request, redis: Redis = Depends(get_redis)):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        captcha = form.get("captcha")
        remember_me = form.get("remember_me")
        if self.enable_captcha:
            captcha_id = request.cookies.get("captcha_id")
            if (
                not captcha
                or await redis.get(constants.CAPTCHA_ID.format(captcha_id=captcha_id)) != captcha
            ):
                return templates.TemplateResponse(
                    self.template,
                    status_code=HTTP_412_PRECONDITION_FAILED,
                    context={"request": request, "error": _("captcha_error")},
                )
        if self.google_recaptcha:
            g_recaptcha_response = form.get("g-recaptcha-response")
            verify_url = self.google_recaptcha.verify_url
            data = {
                "secret": self.google_recaptcha.secret,
                "response": g_recaptcha_response,
                "remoteip": utils.get_client_ip(request),
            }
            async with httpx.AsyncClient() as client:
                res = await client.post(verify_url, data=data)
                ret = res.json()
                if not ret.get("success"):
                    return templates.TemplateResponse(
                        self.template,
                        status_code=HTTP_412_PRECONDITION_FAILED,
                        context={"request": request, "error": _("Google recaptcha verify failed")},
                    )
        admin = await self.admin_model.get_or_none(username=username)
        if not admin or not check_password(password, admin.password):
            return templates.TemplateResponse(
                self.template,
                status_code=HTTP_401_UNAUTHORIZED,
                context={"request": request, "error": _("login_failed")},
            )
        request.state.admin = admin
        response = RedirectResponse(url=request.app.admin_path, status_code=HTTP_303_SEE_OTHER)
        if remember_me == "on":
            expire = constants.LOGIN_EXPIRE
            response.set_cookie("remember_me", "on")
        else:
            expire = 3600
            response.delete_cookie("remember_me")
        token = uuid.uuid4().hex
        response.set_cookie(
            constants.ACCESS_TOKEN,
            token,
            expires=expire,
            path=request.app.admin_path,
            httponly=True,
        )
        await redis.set(constants.LOGIN_USER.format(token=token), admin.pk, ex=expire)
        return response

    async def logout(self, request: Request):
        response = self.redirect_login(request)
        response.delete_cookie(constants.ACCESS_TOKEN, path=request.app.admin_path)
        token = request.cookies.get(constants.ACCESS_TOKEN)
        await request.app.redis.delete(constants.LOGIN_USER.format(token=token))
        return response

    async def authenticate(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ):
        redis = request.app.redis  # type:Redis
        token = request.cookies.get(constants.ACCESS_TOKEN)
        path = request.scope["path"]
        admin = None
        if token:
            token_key = constants.LOGIN_USER.format(token=token)
            admin_id = await redis.get(token_key)
            admin = await self.admin_model.get_or_none(pk=admin_id)
        if admin and admin.is_superuser:
            admin.role_name = "superuser"
        request.state.admin = admin

        if path == self.login_path and admin:
            return RedirectResponse(url=request.app.admin_path, status_code=HTTP_303_SEE_OTHER)

        response = await call_next(request)
        return response

    async def create_user(self, username: str, password: str, **kwargs):
        return await self.admin_model.create(username=username, password=password, **kwargs)

    async def init_view(self, request: Request):
        exists = await self.admin_model.all().limit(1).exists()
        if exists:
            return self.redirect_login(request)
        return templates.TemplateResponse("init.html", context={"request": request})

    async def init(
        self,
        request: Request,
    ):
        exists = await self.admin_model.all().limit(1).exists()
        if exists:
            return self.redirect_login(request)
        form = await request.form()
        password = form.get("password")
        confirm_password = form.get("confirm_password")
        username = form.get("username")
        if password != confirm_password:
            return templates.TemplateResponse(
                "init.html",
                context={"request": request, "error": _("confirm_password_different")},
            )

        await self.create_user(username, password, is_superuser=True)
        return self.redirect_login(request)

    def redirect_login(self, request: Request):
        return RedirectResponse(
            url=request.app.admin_path + self.login_path, status_code=HTTP_303_SEE_OTHER
        )

    async def password_view(
        self,
        request: Request,
        resources=Depends(get_resources),
    ):
        return templates.TemplateResponse(
            "providers/login/password.html",
            context={
                "request": request,
                "resources": resources,
            },
        )

    async def password(
        self,
        request: Request,
        old_password: str = Form(...),
        new_password: str = Form(...),
        re_new_password: str = Form(...),
        admin: AbstractAdmin = Depends(get_current_admin),
        resources=Depends(get_resources),
    ):
        error = None
        if not check_password(old_password, admin.password):
            error = _("old_password_error")
        elif new_password != re_new_password:
            error = _("new_password_different")
        if error:
            return templates.TemplateResponse(
                "password.html",
                context={"request": request, "resources": resources, "error": error},
            )
        admin.password = new_password
        await admin.save(update_fields=["password"])
        return await self.logout(request)


class OAuth2Provider(Provider):
    name = "oauth2_provider"
    label: str
    icon: str
    authorize_url: str
    token_url: str
    user_url: str

    def __init__(
        self,
        admin_model: Type[AbstractAdmin],
        client_id: str,
        client_secret: str,
        redirect_uri: typing.Optional[str] = None,
        **kwargs,
    ):
        self.admin_model = admin_model
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.kwargs = kwargs

    async def get_admin(self, user_info: dict):
        obj, _ = await self.admin_model.get_or_create(
            username=user_info.get("username"), defaults=dict(password="")
        )
        return obj

    async def login(self, request: Request, code: str, redis: Redis = Depends(get_redis)):
        user_info = await self.get_user_info(code)
        admin = await self.get_admin(user_info)
        request.state.admin = admin
        response = RedirectResponse(url=request.app.admin_path, status_code=HTTP_303_SEE_OTHER)
        token = uuid.uuid4().hex
        response.set_cookie(
            constants.ACCESS_TOKEN,
            token,
            expires=constants.LOGIN_EXPIRE,
            path=request.app.admin_path,
            httponly=True,
        )
        await redis.set(
            constants.LOGIN_USER.format(token=token), admin.pk, ex=constants.LOGIN_EXPIRE
        )
        return response

    async def register(self, app: "FastAPIAdmin"):
        await super(OAuth2Provider, self).register(app)
        oauth2_providers = getattr(app, "oauth2_providers", [])
        oauth2_providers.append(self)
        setattr(app, "oauth2_providers", oauth2_providers)
        app.get(f"/oauth2/{self.name}")(self.login)

    async def get_access_token(self, code: str) -> str:
        async with httpx.AsyncClient(headers={"Accept": "application/json"}, timeout=30) as client:
            res = await client.post(self.token_url, data=self.get_access_token_params(code))
            ret = res.json()
            return ret.get("access_token")

    async def get_user_info(self, code: str):
        raise NotImplementedError

    def get_access_token_params(self, code: str):
        return {"client_id": self.client_id, "client_secret": self.client_secret, "code": code}

    def get_authorize_url(self):
        params = {"client_id": self.client_id}
        if self.redirect_uri:
            params["redirect_uri"] = self.redirect_uri
        params.update(self.kwargs)
        return self.authorize_url + "?" + urlencode(params)


class GitHubOAuth2Provider(OAuth2Provider):
    name = "github_oauth2_provider"
    label = "Login with Github"
    icon = "fab fa-github fa-lg"
    authorize_url = "https://github.com/login/oauth/authorize"
    token_url = "https://github.com/login/oauth/access_token"
    user_url = "https://api.github.com/user"

    def __init__(
        self, admin_model: Type[AbstractAdmin], client_id: str, client_secret: str, **kwargs
    ):
        super().__init__(
            admin_model,
            client_id,
            client_secret,
            **kwargs,
        )

    async def get_user_info(self, code: str):
        """
        {
           "login": "long2ice",
           "id": 13377178,
           "node_id": "MDQ6VXNlcjEzMzc3MTc4",
           "avatar_url": "https://avatars.githubusercontent.com/u/13377178?v=4",
           "gravatar_id": "",
           "url": "https://api.github.com/users/long2ice",
           "html_url": "https://github.com/long2ice",
           "followers_url": "https://api.github.com/users/long2ice/followers",
           "following_url": "https://api.github.com/users/long2ice/following{/other_user}",
           "gists_url": "https://api.github.com/users/long2ice/gists{/gist_id}",
           "starred_url": "https://api.github.com/users/long2ice/starred{/owner}{/repo}",
           "subscriptions_url": "https://api.github.com/users/long2ice/subscriptions",
           "organizations_url": "https://api.github.com/users/long2ice/orgs",
           "repos_url": "https://api.github.com/users/long2ice/repos",
           "events_url": "https://api.github.com/users/long2ice/events{/privacy}",
           "received_events_url": "https://api.github.com/users/long2ice/received_events",
           "type": "User",
           "site_admin": false,
           "name": "long2ice",
           "company": "EASI",
           "blog": "https://blog.long2ice.io",
           "location": "ChongQing",
           "email": "long2ice@gmail.com",
           "hireable": true,
           "bio": null,
           "twitter_username": "long2ice",
           "public_repos": 17,
           "public_gists": 3,
           "followers": 55,
           "following": 0,
           "created_at": "2015-07-17T07:14:18Z",
           "updated_at": "2021-05-09T12:28:06Z"
         }
        """
        token = await self.get_access_token(code)
        async with httpx.AsyncClient(
            headers={"Authorization": f"token {token}"}, timeout=30
        ) as client:
            res = await client.get(self.user_url)
            ret = res.json()
            return ret


class GoogleOAuth2Provider(OAuth2Provider):
    name = "google_oauth2_provider"
    label = "Login with Google"
    icon = "fab fa-google fa-lg"
    authorize_url = "https://accounts.google.com/o/oauth2/v2/auth"
    token_url = "https://oauth2.googleapis.com/token"
    user_url = "https://www.googleapis.com/oauth2/v3/userinfo"

    def __init__(
        self,
        admin_model: Type[AbstractAdmin],
        client_id: str,
        client_secret: str,
        response_type: str = "code",
        scopes: typing.List[str] = None,
        **kwargs,
    ):
        if scopes is None:
            scopes = [
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/userinfo.email",
            ]
        scope = " ".join(scopes)
        super().__init__(
            admin_model,
            client_id,
            client_secret,
            scope=scope,
            response_type=response_type,
            **kwargs,
        )

    def get_access_token_params(self, code: str):
        return {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "redirect_uri": self.redirect_uri,
            "grant_type": "authorization_code",
        }

    async def get_user_info(self, code: str):
        """
        {
          "sub": "106299640218962388346",
          "name": "\\u5f6d\\u91d1\\u9f99",
          "given_name": "\\u91d1\\u9f99",
          "family_name": "\\u5f6d",
          "picture": "https://lh3.googleusercontent.com/a-/AOh14GgKPG8D99nx24MaHI512pBsg3kTfx0Cbz-HgTs0gg=s96-c",
          "email": "long2ice@gmail.com",
          "email_verified": true,
          "locale": "zh-CN"
        }
        """
        token = await self.get_access_token(code)
        async with httpx.AsyncClient(
            headers={"Authorization": f"Bearer {token}"}, timeout=30
        ) as client:
            res = await client.get(self.user_url)
            ret = res.json()
            return ret
