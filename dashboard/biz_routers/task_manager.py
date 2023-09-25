from datetime import datetime

# from typing import Type
# from urllib.parse import parse_qs
from uuid import uuid4

from fastapi import APIRouter, Depends, Path
from jinja2 import TemplateNotFound
from starlette.requests import Request
from tortoise import Model

from dashboard.biz_models import DataSet, LabelPage, LabelResult, TaskManage
from dashboard.tools.statistic import statistic_dataset
from dashboard.utils.string_utils import split_string_to_list
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
    (volume, qa_num, word_cnt, qa_records) = statistic_dataset(json_data["fileName"])
    # 将数据插入进dataset表中，这一个步骤我只能理解为将实际的数据按规则写入到表中
    # {'fileName': 'test.csv',
    #  'fileContent': 'question,correct_ans\r\nWhat is the capital of France?,Paris\r\nWho painted the Mona Lisa?,Leonardo da Vinci\r\nWhat is the symbol for the chemical element iron?,Fe\r\n"Who wrote the play ""Hamlet""?",William Shakespeare\r\nWhat is the largest planet in our solar system?,Jupiter\r\nWho is the author of the Harry Potter book series?,J.K. Rowling\r\nWhat is the square root of 64?,8\r\nIn which country is the Taj Mahal located?,India\r\nWho is the current President of the United States?,Joe Biden\r\nWhat is the chemical formula for water?,H2O\r\n"Which animal is known as the ""King of the Jungle""?",Lion\r\nWhat is the tallest mountain in the world?,Mount Everest\r\nWho invented the telephone?,Alexander Graham Bell\r\nWhat is the primary language spoken in Brazil?,Portuguese\r\nWho painted the ceiling of the Sistine Chapel?,Michelangelo\r\n',
    #  'annotationTypes': ['boundingBox'],
    #  'deadline': '2023-09-25T17:12',
    #  'taskAssignments': [{'annotator': '标注员1', 'taskCount': '10'}, {'annotator': '标注员2', 'taskCount': '15'}, {'annotator': '标注员3', 'taskCount': '20'}]}

    dataset_uid = uuid4()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    await DataSet(
        name=json_data["fileName"],
        focused_risks=[{"level1": 1, "name": "国家安全", "description": "null"}],
        url="null",
        file="null",  # url和file都是两个意义不明的字段，后面都将raw data放入到了qa_records中，有没有上面两个字段都无意义
        volume="1GB",
        used_by=10,  # TODO 这个字段没意义，展示留着
        qa_num=10,
        word_cnt=200,
        updated_at="null",  # TODO, 这个字段没有意义
        qa_records=json_data["fileContent"],
        conversation_start_id="0",
        current_conversation_index=0,
        current_qa_record_id=0,
        uid=dataset_uid,  # 这一步意义不明，为什么一个数据集需要用一个uuid作为索引，使用name不行吗
        description="null",  # 这一步意义不明，为什么需要有数据的描述，
        creator="root",  # 如果有多个任务创建者，这个字段是有意义的
        editor="null",  # 目前就没有这个角色，字段意义不明
        reviewer="null",  # 意义不明的字段
        created_at=current_time,
        permissions="null",  # 自相矛盾的字段，意义不明
    ).save()

    # # # 将这个表单数据写入到task表中
    task_id = uuid4()
    await TaskManage(
        task_id=task_id,
        task_type="数据集标注",
        labeling_method=json_data["annotationTypes"],
        current_status="未标注",
        dateset=json_data["fileName"],
        dataset_uid=dataset_uid,
        create_time=current_time,
        end_time=json_data["deadline"],
        assign_user=json_data["taskAssignments"],
    ).save()

    # 将task写入到labelpage中
    await LabelPage(
        task_id=task_id,
        task_type="数据集标注",
        labeling_method=json_data["annotationTypes"],
        current_status="未标注",
        dateset=json_data["fileName"],
        dataset_uid=dataset_uid,
        end_time=json_data["deadline"],
    ).save()

    qa_list = split_string_to_list(json_data["fileContent"])
    # 创建一个task res表，将这个任务的结果存放起来
    for index, (question, answer) in enumerate(qa_list):
        await LabelResult(
            task_id=task_id,
            dataset_id=dataset_uid,
            creator="root",
            question_id=index + 1,
            question=question,
            answer=answer,
        ).save()
    return "success"


@router.get("/{resource}/get_datasets_name")
async def get_datasets_name(request: Request, resources=Depends(get_resources)):
    return ["test1", "test2"]
