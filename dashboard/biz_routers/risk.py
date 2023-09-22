from fastapi import APIRouter, Depends, Path
from starlette.requests import Request

from dashboard.biz_models import Risk
from last.services.depends import get_model_resource, get_resources
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


@router.get("/{resource}/edit/{pk}")
async def edit(
    request: Request,
    resource: str = Path(...),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
    pk: str = Path(...),
):
    # 通过id = pk获取当前一条数据
    context = {
        "request": request,
        "resource": resource,
        "resource_label": model_resource.label,
        "resources": resources,
        "model_resource": model_resource,
        "page_title": "更新维度",
        "pk": pk,
    }
    return templates.TemplateResponse(
        f"{resource}/risk_edit.html",
        context=context,
    )


@router.get("/{resource}")
async def risk(
        request: Request,
        resources=Depends(get_resources),
):
    risks = await Risk.all()

    return templates.TemplateResponse(
        "risk/risk.html",
        context={
            "request": request,
            "resources": resources,
            "page_title": "风险维度",
            "eval_plans": risks,
        },
    )