from enum import Enum
from typing import Type, Union

from fastapi import APIRouter, Depends, Path
from starlette.requests import Request
from tortoise import Model
from tortoise.transactions import in_transaction

from dashboard.biz_models import DataSet
from dashboard.utils.converter import DataSetTool
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

router = APIRouter()


# datamanager


@router.get("/{resource}/epm_create")
async def create_view(
    request: Request,
    resource: str = Path(...),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
):
    """
    page location: create button on the evaluation plan management page
    upstream dependency: evaluation plan management page
    downstream dependency: evaluation model, dataset model
    input example: GET /{resource}/epm_create
    output example: {resource}/create.html
    """
    inputs = await model_resource.get_inputs(request)
    datasets = await DataSet.all().order_by("id").limit(50)
    dataset_schemas = await DataSetTool.ds_model_to_eval_plan_schema(datasets)
    context = {
        "request": request,
        "resources": resources,
        "resource_label": model_resource.label,
        "resource": resource,
        "inputs": inputs,
        "model_resource": model_resource,
        "page_title": model_resource.page_title,
        "page_pre_title": model_resource.page_pre_title,
        "datasets": dataset_schemas,
    }
    return templates.TemplateResponse(
        f"{resource}/create.html",
        context=context,
    )


@router.post(
    "/{resource}/epm_create",
    dependencies=[Depends(admin_log_create), Depends(create_checker)],
)
async def create(
    request: Request,
    resource: str = Path(...),
    model_resource: ModelResource = Depends(get_model_resource),
    model: Type[Model] = Depends(get_model),
):
    """
    page location: save button on the evaluation plan create page
    upstream dependency: evaluation plan create page
    downstream dependency: evaluation model, dataset model
    input example:
        POST /{resource}/epm_create
        {
          "name": "test",
          "plan_content": "国家安全/50.0%/50.0%,个人权利/50.0%/50.0%",
          "score_way": 0,
          "datasets": "1,2",
        }
    output example: {resource}/list.html
    """
    form = await request.form()
    data, m2m_data = await model_resource.resolve_data(request, form)
    async with in_transaction() as conn:
        obj = await model.create(**data, using_db=conn)
        request.state.pk = obj.pk
        for k, items in m2m_data.items():
            m2m_obj = getattr(obj, k)
            await m2m_obj.add(*items, using_db=conn)
        return redirect(request, "list_view", resource=resource)


@router.post(
    "/{resource}/epm_update/{pk}",
    dependencies=[Depends(admin_log_update), Depends(update_checker)],
)
async def update(
    request: Request,
    resource: str = Path(...),
    pk: str = Path(...),
    model_resource: ModelResource = Depends(get_model_resource),
    model: Type[Model] = Depends(get_model),
):
    """
    page location: save button on the evaluation plan create page
    upstream dependency: evaluation plan update page
    downstream dependency: evaluation model, dataset model
    input example:
        POST /{resource}/epm_create/1
        {
          "name": "test",
          "plan_content": "国家安全/50.0%/50.0%,个人权利/50.0%/50.0%",
          "score_way": 0,
          "datasets": "1,2",
        }
    output example: {resource}/list.html
    """
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
    return redirect(request, "list_view", resource=resource)


@router.get("/{resource}/epm_update/{pk}", dependencies=[Depends(read_checker)])
async def update_view(
    request: Request,
    resource: str = Path(...),
    pk: str = Path(...),
    model_resource: ModelResource = Depends(get_model_resource),
    resources=Depends(get_resources),
    model: Type[Model] = Depends(get_model),
):
    """
    page location: edit button on the evaluation plan management page
    upstream dependency: evaluation plan edit page
    downstream dependency: evaluation model, dataset model
    input example: GET /{resource}/epm_create/1
    output example: {resource}/update.html
    """
    obj = await model.get(pk=pk).prefetch_related(*model_resource.get_m2m_field())
    inputs = await model_resource.get_inputs(request, obj)
    datasets = await DataSet.filter(id__in=obj.dataset_ids.split(",")).order_by("id").limit(50)
    dataset_schemas = await DataSetTool.ds_model_to_eval_plan_schema(datasets)
    context = {
        "request": request,
        "resources": resources,
        "resource_label": model_resource.label,
        "resource": resource,
        "inputs": inputs,
        "pk": pk,
        "model_resource": model_resource,
        "datasets": dataset_schemas,
        "obj": obj,
        "page_title": model_resource.page_title,
        "page_pre_title": model_resource.page_pre_title,
    }
    return templates.TemplateResponse(
        f"{resource}/update.html",
        context=context,
    )


@router.get("/{resource}/epm_copy_create/{pk}")
async def copy_create_view(
    request: Request,
    resource: str = Path(...),
    pk: str = Path(...),
    model_resource: ModelResource = Depends(get_model_resource),
    resources=Depends(get_resources),
    model: Type[Model] = Depends(get_model),
):
    """
    page location: copy create button on the evaluation plan management page
    upstream dependency: evaluation plan copy create page
    downstream dependency: evaluation model, dataset model
    input example: GET /{resource}/epm_create/1
    output example: {resource}/copy_create.html
    """
    obj = await model.get(pk=pk).prefetch_related(*model_resource.get_m2m_field())
    inputs = await model_resource.get_inputs(request, obj)
    datasets = await DataSet.all().order_by("id").limit(50)
    dataset_schemas = await DataSetTool.ds_model_to_eval_plan_schema(datasets)
    context = {
        "request": request,
        "resources": resources,
        "resource_label": model_resource.label,
        "resource": resource,
        "inputs": inputs,
        "pk": pk,
        "model_resource": model_resource,
        "datasets": dataset_schemas,
        "obj": obj,
        "page_title": model_resource.page_title,
        "page_pre_title": model_resource.page_pre_title,
    }
    return templates.TemplateResponse(
        f"{resource}/copy_create.html",
        context=context,
    )


@router.post(
    "/{resource}/epm_copy_create",
    dependencies=[Depends(admin_log_update), Depends(update_checker)],
)
async def copy_create(
    request: Request,
    resource: str = Path(...),
    model_resource: ModelResource = Depends(get_model_resource),
    model: Type[Model] = Depends(get_model),
):
    """
    page location: save button on the copy create page
    upstream dependency: evaluation plan copy create page
    downstream dependency: evaluation model, dataset model
    input example:
        POST /{resource}/epm_copy_create
        {
          "name": "test",
          "plan_content": "国家安全/50.0%/50.0%,个人权利/50.0%/50.0%",
          "score_way": 0,
          "datasets": "1,2",
        }
    output example: {resource}/list.html
    """
    form = await request.form()
    data, m2m_data = await model_resource.resolve_data(request, form)
    async with in_transaction() as conn:
        obj = await model.create(**data, using_db=conn)
        request.state.pk = obj.pk
        for k, items in m2m_data.items():
            m2m_obj = getattr(obj, k)
            await m2m_obj.add(*items, using_db=conn)
        return redirect(request, "list_view", resource=resource)


@router.post("/{resource}/epm_ds_query", dependencies=[Depends(read_checker)])
async def epm_ds_query(
    request: Request, ds_name: Union[str, None] = None, ds_content: Union[str, None] = None
):
    """
    page location: datasets search btn on evaluation plan create page、update page and copy create page
    upstream dependency: evaluation plan create page、update page and copy create page
    downstream dependency: evaluation model, dataset model
    input example:
        POST /{resource}/epm_copy_create/1
        {
          "name": "test",
          "plan_content": "国家安全/50.0%/50.0%,个人权利/50.0%/50.0%",
          "score_way": 0,
          "datasets": "1,2",
        }
    output example:
        [
            {
                "risk_type": "国家安全",
                "risk_third_type": "个人信息保护",
                "name": "11",
                "risk_second_type": "颠覆国家政权",
                "id": 1
            }
        ]
    """
    datasets = []
    if ds_name is not None:
        datasets = await DataSet.all().filter(name=ds_name).order_by("id")
    if ds_content is not None:
        datasets = await DataSet.all().filter(name=ds_content).order_by("id")
    if not datasets:
        datasets = await DataSet.all().order_by("id")
    dataset_schemas = await DataSetTool.ds_model_to_eval_plan_schema(datasets)
    return dataset_schemas


# datamanager end


class RiskType(Enum):
    national_security = 0, "国家安全"
    personal_security = 1, "个人安全"

    def __init__(self, code, desc):
        self._code = code
        self._desc = desc

    @property
    def desc(self):
        return self._desc

    @property
    def code(self):
        return self._code
