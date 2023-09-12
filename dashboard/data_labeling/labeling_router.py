from enum import Enum
from fastapi import APIRouter, Depends, Path

from starlette.requests import Request
from tortoise import Model, fields
from tortoise.transactions import in_transaction
from typing import Type

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
from last.services.responses import redirect
from last.services.template import templates
from jinja2 import TemplateNotFound
router = APIRouter()


@router.get("/{resource}/labeling/{pk}")
async def labeling_view(
    request: Request,
    resource: str = Path(...),
    pk: str = Path(...),
    model_resource: ModelResource = Depends(get_model_resource),
    resources=Depends(get_resources),
    model: Type[Model] = Depends(get_model),
):
    obj = await model.get(pk=pk).prefetch_related(*model_resource.get_m2m_field())
    inputs = await model_resource.get_inputs(request, obj)

    # TODO, @xiaomin, 将这个请求里面的参数传递给label.html，从而生成不同的标注页面形式
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
            f"{resource}/label.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "label.html",
            context=context,
        )


@router.get("/{resource}/labeling/get_config")
async def get_config_from_db(
    request: Request,
    resource: str
):

    """_summary_
    # 需要返回 id，支持数据库的搜索

    Args:
        request (Request): _description_
        resource (str): _description_
    """

    mock_data = {
        "tag": [{
                        "value": 'Person',
                        "background": 'red'
                    },
                    {
                        "value": 'Organization',
                        "background": 'darkorange'
                    }],
        "text": "这是一段测试文本"
    }

    return mock_data
