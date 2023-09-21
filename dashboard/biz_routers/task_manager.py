# from datetime import datetime
# from typing import Type
# from urllib.parse import parse_qs
# from uuid import uuid4

from fastapi import APIRouter, Depends, Path
from jinja2 import TemplateNotFound
from starlette.requests import Request
from tortoise import Model

from dashboard.biz_models import DataSet, TaskManage
from dashboard.tools.statistic import statistic_dataset
from last.services.depends import create_checker, get_model, get_model_resource, get_resources
from last.services.resources import Model as ModelResource

# from last.services.routes.resources import list_view
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
    # TODO, 这个位置分配任务，那么如何给某个用户的表创建数据？
    # volume, qa_num, word_cnt, qa_records
    # await DataSet(
    #     name= json_data.fileName,
    #     fouces_risks = [
    #         {"level": 1, "name": "国家安全", "description": "null"},
    #         {"level": 2, "name": "颠覆国家政权", "description": "null", "downlevel_risk_name": ["反政府组织"]}
    #     ], # TODO,这个位置我暂时是写死的，如果这个风险维度就是死的，那么从环境变量中读取
    #     url = "null",
    #     file = "null",
    #     volume = "10GB", # TODO 这个文件大小的统计需要调用本地函数完成
    #     used_by = 100, # TODO,如何计算这个文件被多少个人使用过了
    #     qa_num = 5, # TODO, 同理，这个qa的数据也是没有办法被
    #     ).save()
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
