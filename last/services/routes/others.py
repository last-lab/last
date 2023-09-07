from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from last.services import enums
from last.services.template import get_global_env, set_global_env, templates
router = APIRouter()


@router.get("/maintenance")
async def maintenance(request: Request):
    return templates.TemplateResponse("errors/maintenance.html", context={"request": request})


@router.get("/layout")
async def switch_layout(request: Request):
    layout = enums.Layout(get_global_env("layout"))
    response = RedirectResponse(url=request.headers.get("referer"), status_code=HTTP_303_SEE_OTHER)
    if layout == enums.Layout.layout:
        set_global_env("layout", str(enums.Layout.layout_navbar))
        response.set_cookie("layout", enums.Layout.layout_navbar)
    else:
        set_global_env("layout", str(enums.Layout.layout))
        response.set_cookie("layout", enums.Layout.layout, httponly=True)
    return response


@router.get("/stable1")
async def stable1(request: Request):
    table_1 = [
        {"name": "Alice", "age": 25, "city": "New York"},
        {"name": "Bob", "age": 30, "city": "London"},
        {"name": "Charlie", "age": 28, "city": "Paris"},
        {"name": "David", "age": 35, "city": "Tokyo"},
        {"name": "Emily", "age": 29, "city": "Sydney"},
        {"name": "Frank", "age": 33, "city": "Berlin"},
        {"name": "Grace", "age": 27, "city": "Toronto"},
        {"name": "Henry", "age": 31, "city": "Moscow"},
        {"name": "Isabella", "age": 26, "city": "Rome"},
        {"name": "Jack", "age": 32, "city": "Seoul"}
    ]


    return templates.TemplateResponse("stable/stable1.html", context={"request": request, "stable_1": table_1})

@router.get("/stable2")
async def stable2(request: Request):

    return templates.TemplateResponse("stable/text_annotation_example.html", context={"request": request})