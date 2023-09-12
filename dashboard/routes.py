from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_404_NOT_FOUND

from dashboard.biz_routers import biz_router, labeling_router

from dashboard.models import Config, Log
from last.services.app import app
from last.services.depends import AdminLog, get_resources
from last.services.i18n import _
from last.services.routes.others import router
from last.services.template import templates

app.include_router(labeling_router)
app.include_router(biz_router)



@app.get("/")
async def home(
    request: Request,
    resources=Depends(get_resources),
):
    logs = (
        await Log.all()
        .limit(9)
        .order_by("-id")
        .values(
            "resource",
            "action",
            "content",
            "created_at",
            username="admin__username",
            avatar="admin__avatar",
        )
    )
    return templates.TemplateResponse(
        "dashboard.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "dashboard",
            "page_pre_title": "overview",
            "page_title": "Dashboard",
            "logs": logs,
        },
    )


@app.get("/notification")
async def notification(
    request: Request,
    resources=Depends(get_resources),
):
    return templates.TemplateResponse(
        "notification.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Notification",
            "page_pre_title": "Notification",
            "page_title": "Send notification",
        },
    )


@app.get("/label")
async def label(
    request: Request,
    resources=Depends(get_resources),
):
    return templates.TemplateResponse(
        "label.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Label",
            "page_pre_title": "BY LABEL STUDIO",
            "page_title": "Label",
        },
    )


@app.get("/record/add")
async def create_eval(
    request: Request,
    resources=Depends(get_resources),
):
    return templates.TemplateResponse(
        "create_eval.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Label",
            "page_pre_title": "BY LABEL STUDIO",
            "page_title": _("Create Evaluation"),
            "eval_plans": [
                {
                    "plan_name": "Plan 1",
                    "plan_content": "Plan 1 content",
                },
                {
                    "plan_name": "Plan 2",
                    "plan_content": "Plan 2 content",
                },
                {
                    "plan_name": "Plan 3",
                    "plan_content": "Plan 3 content",
                },
            ],
            "eval_models": [
                {
                    "name": "Model 1",
                    "model_content": "Model 1 content",
                    "uid": "1",
                },
                {
                    "name": "Model 2",
                    "model_content": "Model 2 content",
                    "uid": "2",
                },
                {
                    "name": "Model 3",
                    "model_content": "Model 3 content",
                    "uid": "3",
                },
                {
                    "name": "Model 4",
                    "model_content": "Model 4 content",
                    "uid": "4",
                },
            ],
        },
    )


admin_log_config_switch_status = AdminLog(action="config_status_switch")


@app.put("/{resource}/switch_status/{pk}", dependencies=[Depends(admin_log_config_switch_status)])
async def switch_config_status(request: Request, pk: str):
    config = await Config.get_or_none(pk=pk)
    if not config:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    config.status = not config.status
    await config.save(update_fields=["status"])
    return RedirectResponse(url=request.headers.get("referer"), status_code=HTTP_303_SEE_OTHER)


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
        {"name": "Jack", "age": 32, "city": "Seoul"},
    ]

    return templates.TemplateResponse(
        "stable/stable1.html", context={"request": request, "stable_1": table_1}
    )

    # try:
    #     return templates.TemplateResponse(
    #         f"{resource}/update.html",
    #         context=context,
    #     )
    # except TemplateNotFound:
    #     return templates.TemplateResponse(
    #         "update.html",
    #         context=context,
    #     )
