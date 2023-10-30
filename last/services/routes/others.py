from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from last.services import enums
from last.services.template import get_global_env, set_global_env, templates

router = APIRouter()


@router.get("/maintenance")
async def maintenance(request: Request):
    return templates.TemplateResponse(
        "errors/maintenance.html", context={"request": request}
    )


@router.get("/layout")
async def switch_layout(request: Request):
    layout = enums.Layout(get_global_env("layout"))
    response = RedirectResponse(
        url=request.headers.get("referer"), status_code=HTTP_303_SEE_OTHER
    )
    if layout == enums.Layout.layout:
        set_global_env("layout", str(enums.Layout.layout_navbar))
        response.set_cookie("layout", enums.Layout.layout_navbar)
    else:
        set_global_env("layout", str(enums.Layout.layout))
        response.set_cookie("layout", enums.Layout.layout, httponly=True)
    return response
