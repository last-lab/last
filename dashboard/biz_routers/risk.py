from fastapi import APIRouter, Depends, Path
from starlette.requests import Request

from dashboard.biz_models import Risk
from dashboard.utils.util import Tool
from last.services.depends import get_model_resource, get_resources
from last.services.resources import Model as ModelResource
from last.services.template import templates

router = APIRouter()


# 新建风险维度的路由（尚未开发）
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


# 编辑风险维度的路由（尚未开发）
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


# 风险维度的路由
@router.get("/risk")
async def get_risk(
    request: Request,
    resources=Depends(get_resources),
):
    risks = await Risk.all().filter(risk_level=1)
    for first_risk in risks:
        # 获取二级风险
        second_risks = await Risk.all().filter(risk_level=2, parent_risk_id=first_risk.risk_id)
        first_risk.second_risks = second_risks
        first_risk.dataset = await Tool.get_dataset_match_risk(first_risk)
        for second_risk in second_risks:
            # 获取三级风险
            third_risks = await Risk.all().filter(risk_level=3, parent_risk_id=second_risk.risk_id)
            second_risk.third_risks = third_risks
            second_risk.dataset = await Tool.get_dataset_match_risk(second_risk)
            for third_risk in third_risks:
                third_risk.dataset = await Tool.get_dataset_match_risk(third_risk)
    context = {
        "request": request,
        "resources": resources,
        "resource_label": "Label",
        "page_title": "风险维度",
        "risks": risks,
    }
    return templates.TemplateResponse(
        "risk/risk.html",
        context=context,
    )
