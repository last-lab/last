from fastapi import APIRouter, Depends, Path
from jinja2 import TemplateNotFound
from starlette.requests import Request

from last.services.depends import get_resources, get_model_resource
from last.services.resources import Model as ModelResource
from last.services.template import templates

router = APIRouter()


@router.get("/{resource}/risk_create")
async def risk_create(
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
        "page_title": "新建维度",
    }
    return templates.TemplateResponse(
        f"{resource}/risk_create.html",
        context=context,
    )


# @router.get("/{resource}/edit/{pk}")
# async def edit(
#         request: Request,
#         resource: str = Path(...),
#         resources=Depends(get_resources),
#         model_resource: ModelResource = Depends(get_model_resource),
#         pk: str = Path(...),
# ):
#     context = {
#         "request": request,
#         "resource": resource,
#         "resource_label": model_resource.label,
#         "resources": resources,
#         "model_resource": model_resource,
#         "page_title": "更新维度",
#         "pk": pk
#     }
#     return templates.TemplateResponse(
#         f"{resource}/risk_edit.html",
#         context=context,
#     )
