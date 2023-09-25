from fastapi import APIRouter, Depends, Path
from starlette.requests import Request

from dashboard.biz_models import DataSet, Risk
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


@router.get("/risk")
async def get_risk(
    request: Request,
    resources=Depends(get_resources),
):
    risks = await Risk.all().filter(risk_level=1)
    for first_risk in risks:
        second_risks = await Risk.all().filter(risk_level=2, parent_risk_id=first_risk.risk_id)
        first_risk.second_risks = second_risks
        datasets = await DataSet.all().filter(first_risk_id=first_risk.risk_id)
        first_risk.dataset = {
            "dataset_count": len(datasets),
            "dataset_word_cnt": sum([obj.word_cnt for obj in datasets]),
            "dataset_name_list": [obj.name for obj in datasets],
        }
        for second_risk in second_risks:
            third_risks = await Risk.all().filter(risk_level=3, parent_risk_id=second_risk.risk_id)
            second_risk.third_risks = third_risks
            second_dataset = []
            datasets = await DataSet.all().filter()
            for dataset in datasets:
                if second_risk.risk_id in dataset.focused_risks:
                    second_dataset.append(dataset)
            second_risk.dataset = {
                "dataset_count": len(second_dataset),
                "dataset_word_cnt": sum([obj.word_cnt for obj in second_dataset]),
                "dataset_name_list": [obj.name for obj in second_dataset],
            }
            for third_risk in third_risks:
                third_dataset = []
                datasets = await DataSet.all().filter()
                for dataset in datasets:
                    if third_risk.risk_id in dataset.focused_risks:
                        third_dataset.append(dataset)
                third_risk.dataset = {
                    "dataset_count": len(third_dataset),
                    "dataset_word_cnt": sum([obj.word_cnt for obj in third_dataset]),
                    "dataset_name_list": [obj.name for obj in third_dataset],
                }
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
