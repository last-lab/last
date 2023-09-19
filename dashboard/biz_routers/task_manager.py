from typing import Type
from uuid import uuid4
from datetime import datetime

from urllib.parse import parse_qs
from fastapi import APIRouter, Depends, Path
from jinja2 import TemplateNotFound
from starlette.requests import Request
from tortoise import Model
from dashboard.biz_models import TaskManage
from last.services.depends import get_model, get_model_resource, get_resources
from last.services.depends import create_checker
from last.services.resources import Model as ModelResource
from last.services.template import templates
from last.services.routes.resources import list_view
router = APIRouter()


@router.get("/{resource}/create_task", dependencies=[Depends(create_checker)])
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
        "page_title": "创建标注任务",
    }
    try:
        return templates.TemplateResponse(
            f"{resource}/create_task.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "create_task.html",
            context=context,
        )


@router.post("/{resource}/create_task_callback")
async def create_task_callback(
    request: Request,
    model: Model = Depends(get_model),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
    resource: str = Path(...)
    ):
    form_data = await request.form()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # # 将这个表单数据写入到task表中
    await TaskManage(
        task_id = uuid4(),
        labeling_method = form_data['labeling_method'],
        dateset = form_data["dataset_name"],
        create_time = current_time,
        current_status = "未标注",
    ).save()
    return "success"




@router.get("/{resource}/get_datasets_name")
async def get_datasets_name(
    request: Request,
    resources = Depends(get_resources)
):
    return ["test1", "test2"]
