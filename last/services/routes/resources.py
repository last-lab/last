from typing import Type

from fastapi import APIRouter, Depends, Path
from jinja2 import TemplateNotFound
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from tortoise import Model

# from tortoise.fields import ManyToManyRelation
from tortoise.transactions import in_transaction

from last.services.depends import (
    admin_log_create,
    admin_log_delete,
    admin_log_update,
    create_checker,
    delete_checker,
    get_model,
    get_model_resource,
    get_resources,
    read_checker,
    update_checker,
)
from last.services.resources import Model as ModelResource
from last.services.resources import render_values
from last.services.responses import redirect
from last.services.template import templates

router = APIRouter()


@router.get("/{resource}/list", dependencies=[Depends(read_checker)])
async def list_view(
    request: Request,
    model: Model = Depends(get_model),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
    resource: str = Path(...),
    page_size: int = 10,
    page_num: int = 1,
):
    fields_label = model_resource.get_fields_label()
    fields = model_resource.get_fields()
    qs = model.all()
    params, qs = await model_resource.resolve_query_params(
        request, dict(request.query_params), qs
    )
    filters = await model_resource.get_filters(request, params)
    total = await qs.count()
    if page_size:
        qs = qs.limit(page_size)
    else:
        page_size = model_resource.page_size
    qs = qs.offset((page_num - 1) * page_size)
    values = await qs.values()
    (
        rendered_values,
        row_attributes,
        column_attributes,
        cell_attributes,
    ) = await render_values(request, model_resource, fields, values)
    context = {
        "request": request,
        "resources": resources,
        "fields_label": fields_label,
        "fields": fields,
        "values": values,
        "rendered_values": rendered_values,
        "row_attributes": row_attributes,
        "column_attributes": column_attributes,
        "cell_attributes": cell_attributes,
        "filters": filters,
        "query": request.query_params,
        "resource": resource,
        "model_resource": model_resource,
        "resource_label": model_resource.label,
        "page_size": page_size,
        "page_num": page_num,
        "total": total,
        "from": page_size * (page_num - 1) + 1,
        "to": page_size * page_num,
        "page_title": model_resource.page_title,
        "page_pre_title": model_resource.page_pre_title,
    }
    try:
        return templates.TemplateResponse(
            f"{resource}/list.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "list.html",
            context=context,
        )


@router.post(
    "/{resource}/update/{pk}",
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


@router.get("/{resource}/update/{pk}", dependencies=[Depends(read_checker)])
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


@router.get("/{resource}/create", dependencies=[Depends(create_checker)])
async def create_view(
    request: Request,
    resource: str = Path(...),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
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
    try:
        return templates.TemplateResponse(
            f"{resource}/create.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "create.html",
            context=context,
        )


@router.post(
    "/{resource}/create",
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
    try:
        return templates.TemplateResponse(
            f"{resource}/create.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "create.html",
            context=context,
        )


@router.delete(
    "/{resource}/delete/{pk}",
    dependencies=[Depends(admin_log_delete), Depends(delete_checker)],
)
async def delete_view(request: Request, pk: str, model: Model = Depends(get_model)):
    obj = await model.get(pk=pk)
    await obj.delete()
    return RedirectResponse(
        url=request.headers.get("referer"), status_code=HTTP_303_SEE_OTHER
    )


@router.delete(
    "/{resource}/delete",
    dependencies=[Depends(admin_log_delete), Depends(delete_checker)],
)
async def bulk_delete(request: Request, ids: str, model: Model = Depends(get_model)):
    await model.filter(pk__in=ids.split(",")).delete()
    return RedirectResponse(
        url=request.headers.get("referer"), status_code=HTTP_303_SEE_OTHER
    )
