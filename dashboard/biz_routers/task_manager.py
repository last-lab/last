from datetime import datetime
# from typing import Type
# from urllib.parse import parse_qs
from uuid import uuid4

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
    # TODO，上传的时候，直接将数据的原本内容就直接上传上来就好了？
    # 目前假设管理员和标注员都能访问到某个共享内容，所有的数据集放在这个里面，如cpfs位置，
    # 但是只有管理员才有创建任务的权限
    # TODO, 这个位置分配任务，那么如何给某个用户的表创建数据？
    # 目前就是根据回传回来的taskAssignments字段进行拆分
    #  'taskAssignments': [{'annotator': '标注员1', 'taskCount': '10'},
    #                      {'annotator': '标注员2', 'taskCount': '15'},
    #                      {'annotator': '标注员3', 'taskCount': '20'}]}

    # 默认有一个文件夹存放所有的数据集原始文件，因此只要传入数据的名字就可以了
    volume, qa_num, word_cnt, qa_records = statistic_dataset(json_data.fileName)
    # 将数据插入进dataset表中，这一个步骤我只能理解为将实际的数据按规则写入到表中
    task_uid = uuid4()
    await DataSet(
        name= json_data.fileName,
        url = "null",
        file = "null", # url和file都是两个意义不明的字段，后面都将raw data放入到了qa_records中，有没有上面两个字段都无意义
        volume = volume,
        used_by = 10, #TODO 这个字段没意义，展示留着
        qa_num = qa_num,
        word_cnt = word_cnt,
        updated_at = "null", # TODO, 这个字段没有意义
        qa_records = qa_records,
        conversation_start_id = 0,
        current_conversation_index = 0,
        uid = uuid4(), # 这一步意义不明，为什么一个数据集需要用一个uuid作为索引，使用name不行吗
        description = "null", # 这一步意义不明，为什么需要有数据的描述，
        creator = "root", # 如果有多个任务创建者，这个字段是有意义的
        editor = "null", # 目前就没有这个角色，字段意义不明
        reviewer = "null", # 意义不明的字段
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        permissions = "null" # 自相矛盾的字段，意义不明
        ).save()
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
