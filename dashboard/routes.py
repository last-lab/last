from typing import Type

from fastapi import Depends, File, HTTPException, Path, UploadFile
from jinja2 import TemplateNotFound
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_404_NOT_FOUND
from tortoise import Model
from tortoise.transactions import in_transaction

from dashboard.biz_routers import biz_router
from dashboard.data_labeling import labeling_router
from dashboard.models import Config, Log
from last.services.app import app
from last.services.depends import (
    AdminLog,
    admin_log_update,
    create_checker,
    get_model,
    get_model_resource,
    get_resources,
    read_checker,
    update_checker,
)
from last.services.i18n import _
from last.services.resources import Model as ModelResource
from last.services.responses import redirect
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


# datamanager
@app.get("/{resource}/copy_create/{pk}", dependencies=[Depends(read_checker)])
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
    try:
        return templates.TemplateResponse(
            f"{resource}/copy_create.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "update.html",
            context=context,
        )


@app.post(
    "/{resource}/copy_create/{pk}",
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
            "pk": pk,
            "page_title": model_resource.page_title,
            "page_pre_title": model_resource.page_pre_title,
        }
        try:
            return templates.TemplateResponse(
                f"{resource}/update.html",
                context=context,
            )
        except TemplateNotFound:
            return templates.TemplateResponse(
                "update.html",
                context=context,
            )
    return redirect(request, "list_view", resource=resource)


# @app.post(
#     "/{resource}/create",
#     dependencies=[Depends(admin_log_create), Depends(create_checker)],
# )
# async def create(
#         request: Request,
#         resource: str = Path(...),
#         resources=Depends(get_resources),
#         model_resource: ModelResource = Depends(get_model_resource),
#         model: Type[Model] = Depends(get_model),
# ):
#     inputs = await model_resource.get_inputs(request)
#     form = await request.form()
#     data, m2m_data = await model_resource.resolve_data(request, form)
#     async with in_transaction() as conn:
#         obj = await model.create(**data, using_db=conn)
#         request.state.pk = obj.pk
#         for k, items in m2m_data.items():
#             m2m_obj = getattr(obj, k)  # type:ManyToManyRelation
#             await m2m_obj.add(*items, using_db=conn)
#     if "save" in form.keys():
#         return redirect(request, "list_view", resource=resource)
#     context = {
#         "request": request,
#         "resources": resources,
#         "resource_label": model_resource.label,
#         "resource": resource,
#         "inputs": inputs,
#         "model_resource": model_resource,
#         "page_title": model_resource.page_title,
#         "page_pre_title": model_resource.page_pre_title,
#     }
#     try:
#         return templates.TemplateResponse(
#             f"{resource}/create.html",
#             context=context,
#         )
#     except TemplateNotFound:
#         return templates.TemplateResponse(
#             "create.html",
#             context=context,
#         )
# datamanager end

# @app.post(
#     "/{resource}/search",
#     dependencies=[Depends(admin_log_update), Depends(update_checker)]
# )
# async def get_list(
#         request: Request,
#         resource: str = Path(...),
# ):
#     context = {
#         "request": request,
#         "resources": resource
#     }
#     try:
#         return templates.TemplateResponse(
#             f"{resource}/search.html",
#             context=context,
#         )
#     except TemplateNotFound:
#         return templates.TemplateResponse(
#             "search.html",
#             context=context,
#         )


@app.get("/{resource}/upload_dataset", dependencies=[Depends(create_checker)])
async def upload_dataset(
    request: Request,
    resource: str = Path(...),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
):
    context = {
        "request": request,
        "resource": resource,
        "resource_label": model_resource.label,
        "resources": resources,
        "model_resource": model_resource,
        "page_title": "上传评测集",
    }
    try:
        return templates.TemplateResponse(
            f"{resource}/upload_dataset.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "upload_dataset.html",
            context=context,
        )


@app.post("/evaluationdatasetmanager/json")
async def json(request: Request, file: UploadFile = File(...)):
    contents = {
        "result": 1,
        "reason": "评测集已存在",
        "type": "国家安全",
        "detail": [
            {"subType": "颠覆国家政权", "thirdType": ["三级维度1", "三级维度2"]},
            {"subType": "宣传恐怖主义", "thirdType": ["三级维度3", "三级维度4"]},
        ],
        "dataCount": 666,
        "number": 10000,
        "size": "10.6GB",
    }
    return contents


class Item(BaseModel):
    dataset_name: str


@app.post("/evaluationdatasetmanager/conform")
async def conform(request: Request, item: Item):
    contents = {"result": 1, "reason": "已存在同名的评测集"}
    return contents


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
