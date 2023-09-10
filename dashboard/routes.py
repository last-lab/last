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
