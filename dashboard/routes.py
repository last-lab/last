from fastapi import Depends, HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_404_NOT_FOUND

from dashboard.models import Config, Log
from last.services.app import app
from last.services.depends import AdminLog, get_resources
from last.services.template import templates


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


admin_log_config_switch_status = AdminLog(action="config_status_switch")


@app.put("/{resource}/switch_status/{pk}", dependencies=[Depends(admin_log_config_switch_status)])
async def switch_config_status(request: Request, pk: str):
    config = await Config.get_or_none(pk=pk)
    if not config:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    config.status = not config.status
    await config.save(update_fields=["status"])
    return RedirectResponse(url=request.headers.get("referer"), status_code=HTTP_303_SEE_OTHER)


@app.get("/dataset")
async def dataset(
        request: Request,
        resources=Depends(get_resources),
):
    table_resources = [
        {"name": "评测集名字1", "type": "国家安全", "sub_type": "颠覆国家政权", "updateTime": "2022-11-08 18:00", "useCount": 56},
        {"name": "评测集名字2", "type": "国家安全", "sub_type": "宣传恐怖主义", "updateTime": "2022-11-08 18:00", "useCount": 123},
        {"name": "评测集名字3", "type": "个人权利", "sub_type": "隐私保护", "updateTime": "2022-11-08 18:00", "useCount": 55},
        {"name": "评测集名字4", "type": "合法合规", "sub_type": "侵害肖像权", "updateTime": "2022-11-08 18:00", "useCount": 7},
    ]
    return templates.TemplateResponse(
        "dataset.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Dataset",
            "page_pre_title": "",
            "page_title": "评测集管理",
            "table_resources": table_resources
        },
    )
