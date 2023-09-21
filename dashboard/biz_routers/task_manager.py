# from datetime import datetime
# from typing import Type
from urllib.parse import parse_qs
from uuid import uuid4

from fastapi import APIRouter, Depends, Path
from jinja2 import TemplateNotFound
from starlette.requests import Request
from tortoise import Model

from dashboard.biz_models import DataSet, TaskManage
from last.services.depends import create_checker, get_model, get_model_resource, get_resources
from last.services.resources import Model as ModelResource
from last.services.routes.resources import list_view
from last.services.template import templates

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


@router.post("/{resource}/assign_test_task")
async def assign_test_task(
    request: Request,
    model: Model = Depends(get_model),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
    resource: str = Path(...),
):
    # 分配评测任务给某一个用户的回调函数
    context = {
        "request": request,
        "resource": resource,
        "resource_label": model_resource.label,
        "resources": resources,
        "model_resource": model_resource,
        "page_title": "分配评测任务",
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
    resource: str = Path(...),
):
    json_data = await request.json()
    print(json_data)
    await DataSet(name="").save()
    # 回传回来的数据样例：
    # {'fileName': 'file',
    #  'annotationTypes': ['sorting', 'boundingBox'],
    #  'deadline': '2023-09-21T16:27',
    #  'taskAssignments': [{'annotator': '标注员1', 'taskCount': '10'},
    #                      {'annotator': '标注员2', 'taskCount': '15'},
    #                      {'annotator': '标注员3', 'taskCount': '20'}]}
    # 数据集表添加一个记录，task表添加一个记录，任务结果表添加一个记录

    # current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # # # 将这个表单数据写入到task表中
    # task_id = uuid4()
    # await TaskManage(
    #     task_id = task_id,
    #     labeling_method = form_data['labeling_method'],
    #     dateset = form_data["dataset_name"],
    #     create_time = current_time,
    #     current_status = "未标注",
    # ).save()
    await TaskManage().save()

    # await LabelPage(
    #     task_id = task_id,
    #     labeling_method = form_data['labeling_method'],
    #     dateset = form_data["dataset_name"],
    #     create_time = current_time,
    #     current_status = "未标注",
    # ).save()

    return "success"


@router.get("/{resource}/get_datasets_name")
async def get_datasets_name(request: Request, resources=Depends(get_resources)):
    return ["test1", "test2"]
