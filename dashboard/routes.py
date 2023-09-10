from typing import Type

from fastapi import Depends, Path
from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from starlette.status import HTTP_404_NOT_FOUND
from tortoise import Model
from tortoise.transactions import in_transaction

from dashboard.models import Config, Log
from last.services.app import app
from last.services.depends import AdminLog
from last.services.depends import (
    admin_log_create,
    admin_log_update,
    create_checker,
    get_model,
    get_model_resource,
    get_resources,
    read_checker,
    update_checker,
)
from last.services.resources import Model as ModelResource
from last.services.responses import redirect
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


admin_log_config_switch_status = AdminLog(action="config_status_switch")


@app.put("/{resource}/switch_status/{pk}", dependencies=[Depends(admin_log_config_switch_status)])
async def switch_config_status(request: Request, pk: str):
    config = await Config.get_or_none(pk=pk)
    if not config:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
    config.status = not config.status
    await config.save(update_fields=["status"])
    return RedirectResponse(url=request.headers.get("referer"), status_code=HTTP_303_SEE_OTHER)


# datamanager
@app.post(
    "/evaluationplanmanager/update/{pk}",
    dependencies=[Depends(admin_log_update), Depends(update_checker)],
)
async def update(
        request: Request,
        resource: str = Path(...),
        pk: str = Path(...),
        model_resource: ModelResource = Depends(get_model_resource),
        resources=Depends(get_resources),
        model: Type[Model] = Depends(get_model),
):
    form = await request.form()
    data, m2m_data = await model_resource.resolve_data(request, form)
    async with in_transaction() as conn:
        obj = (
            await model.filter(pk=pk)
            .using_db(conn)
            .select_for_update()
            .get()
            .prefetch_related(*model_resource.get_m2m_field())
        )
        await obj.update_from_dict(data).save(using_db=conn)
        for k, items in m2m_data.items():
            m2m_obj = getattr(obj, k)
            await m2m_obj.clear()
            if items:
                await m2m_obj.add(*items)
        obj = (
            await model.filter(pk=pk)
            .using_db(conn)
            .get()
            .prefetch_related(*model_resource.get_m2m_field())
        )
    inputs = await model_resource.get_inputs(request, obj)
    if "save" in form.keys():
        context = {
            "request": request,
            "resources": resources,
            "resource_label": model_resource.label,
            "resource": resource,
            "model_resource": model_resource,
            "inputs": inputs,
            "pk": pk,
            "page_title": model_resource.page_title,
            "page_pre_title": model_resource.page_pre_title,
        }
        return templates.TemplateResponse(
            f"{resource}/update.html",
            context=context,
        )

    return redirect(request, "list_view", resource=resource)


@app.get("/evaluationplanmanager/update/{pk}", dependencies=[Depends(read_checker)])
async def update_view(
        request: Request,
        resource: str = Path(...),
        pk: str = Path(...),
        model_resource: ModelResource = Depends(get_model_resource),
        resources=Depends(get_resources),
        model: Type[Model] = Depends(get_model),
):
    obj = await model.get(pk=pk).prefetch_related(*model_resource.get_m2m_field())
    inputs = await model_resource.get_inputs(request, obj)
    context = {
        "request": request,
        "resources": resources,
        "resource_label": model_resource.label,
        "resource": resource,
        "inputs": inputs,
        "pk": pk,
        "model_resource": model_resource,
        "page_title": model_resource.page_title,
        "page_pre_title": model_resource.page_pre_title,
    }
    return templates.TemplateResponse(
        f"{resource}/update.html",
        context=context,
    )


@app.get("/evaluationplanmanager/create", dependencies=[Depends(create_checker)])
async def create_view(
        request: Request,
        resource: str = Path(...),
        resources=Depends(get_resources),
        model_resource: ModelResource = Depends(get_model_resource),
        page_size: int = 10,
        page_num: int = 1,
):
    inputs = await model_resource.get_inputs(request)
    context = {
        "request": request,
        "resources": resources,
        "resource_label": model_resource.label,
        "resource": resource,
        "inputs": inputs,
        "model_resource": model_resource,
        "page_title": model_resource.page_title,
        "page_pre_title": model_resource.page_pre_title,
    }
    return templates.TemplateResponse(
        f"{resource}/create.html",
        context=context,
    )


@app.post(
    "/evaluationplanmanager/create",
    dependencies=[Depends(admin_log_create), Depends(create_checker)],
)
async def create(
        request: Request,
        resource: str = Path(...),
        resources=Depends(get_resources),
        model_resource: ModelResource = Depends(get_model_resource),
        model: Type[Model] = Depends(get_model),
):
    inputs = await model_resource.get_inputs(request)
    form = await request.form()
    data, m2m_data = await model_resource.resolve_data(request, form)
    async with in_transaction() as conn:
        obj = await model.create(**data, using_db=conn)
        request.state.pk = obj.pk
        for k, items in m2m_data.items():
            m2m_obj = getattr(obj, k)  # type:ManyToManyRelation
            await m2m_obj.add(*items, using_db=conn)
    if "save" in form.keys():
        return redirect(request, "list_view", resource=resource)
    context = {
        "request": request,
        "resources": resources,
        "resource_label": model_resource.label,
        "resource": resource,
        "inputs": inputs,
        "model_resource": model_resource,
        "page_title": model_resource.page_title,
        "page_pre_title": model_resource.page_pre_title,
    }
    return templates.TemplateResponse(
        f"{resource}/create.html",
        context=context,
    )


@app.get("/evaluationplanmanager/copy_create/{pk}", dependencies=[Depends(read_checker)])
async def copy_create_view(
        request: Request,
        resource: str = Path(...),
        pk: str = Path(...),
        model_resource: ModelResource = Depends(get_model_resource),
        resources=Depends(get_resources),
        model: Type[Model] = Depends(get_model),
):
    obj = await model.get(pk=pk).prefetch_related(*model_resource.get_m2m_field())
    inputs = await model_resource.get_inputs(request, obj)
    context = {
        "request": request,
        "resources": resources,
        "resource_label": model_resource.label,
        "resource": resource,
        "inputs": inputs,
        "pk": pk,
        "model_resource": model_resource,
        "page_title": model_resource.page_title,
        "page_pre_title": model_resource.page_pre_title,
    }
    return templates.TemplateResponse(
        f"{resource}/copy_create.html",
        context=context,
    )


@app.post(
    "/evaluationplanmanager/copy_create/{pk}",
    dependencies=[Depends(admin_log_update), Depends(update_checker)],
)
async def copy_create(
        request: Request,
        resource: str = Path(...),
        pk: str = Path(...),
        model_resource: ModelResource = Depends(get_model_resource),
        resources=Depends(get_resources),
        model: Type[Model] = Depends(get_model),
):
    form = await request.form()
    data, m2m_data = await model_resource.resolve_data(request, form)
    async with in_transaction() as conn:
        obj = (
            await model.filter(pk=pk)
            .using_db(conn)
            .select_for_update()
            .get()
            .prefetch_related(*model_resource.get_m2m_field())
        )
        await obj.update_from_dict(data).save(using_db=conn)
        for k, items in m2m_data.items():
            m2m_obj = getattr(obj, k)
            await m2m_obj.clear()
            if items:
                await m2m_obj.add(*items)
        obj = (
            await model.filter(pk=pk)
            .using_db(conn)
            .get()
            .prefetch_related(*model_resource.get_m2m_field())
        )
    inputs = await model_resource.get_inputs(request, obj)
    if "save" in form.keys():
        context = {
            "request": request,
            "resources": resources,
            "resource_label": model_resource.label,
            "resource": resource,
            "model_resource": model_resource,
            "inputs": inputs,
            "page_title": model_resource.page_title,
            "page_pre_title": model_resource.page_pre_title,
        }
        return templates.TemplateResponse(
            f"{resource}/copy_create.html",
            context=context,
        )

    return redirect(request, "list_view", resource=resource)

# datamanager end
