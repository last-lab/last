from datetime import datetime
from typing import Type

# from typing import Type
# from urllib.parse import parse_qs
from uuid import uuid4

from fastapi import APIRouter, Depends, Path
from jinja2 import TemplateNotFound
from starlette.requests import Request
from tortoise import Model

from dashboard.biz_models import AuditPage, AuditResult, LabelPage, LabelResult, TaskManage
from dashboard.resources import Admin
from dashboard.tools.allocate_task import distribute_audit_task, distribute_labeling_task
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
    # TODO，上传的时候，直接将数据的原本内容就直接上传上来就好了？
    # 目前假设管理员和标注员都能访问到某个共享内容，所有的数据集放在这个里面，如cpfs位置，
    # 但是只有管理员才有创建任务的权限
    # TODO, 这个位置分配任务，那么如何给某个用户的表创建数据？
    (volume, qa_num, word_cnt, qa_records) = statistic_dataset(json_data["fileName"])
    dataset_uid = uuid4()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # df = pd.read_csv(json_data['file'])

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
        audit_user=json_data["auditAssignments"],
    ).save()

    qa_list = split_string_to_list(json_data["fileContent"])
    assign_dict = {user["annotator"]: user["taskCount"] for user in json_data["taskAssignments"]}
    (
        item_assign_user_dict,
        assign_user_item_dict,
        assign_user_item_length,
        assign_user_labeling_progress,
    ) = distribute_labeling_task(len(qa_list), assign_dict)
    labeling_flag = {
        user: [False for _ in range(len(assign_user_item_dict[user]))]
        for user in assign_user_item_dict
    }
    # 将task写入到labelpage中
    await LabelPage(
        task_id=task_id,
        task_type="数据集标注",
        labeling_method=json_data["annotationTypes"],
        dateset=json_data["fileName"],
        dataset_uid=dataset_uid,
        end_time=json_data["deadline"],
        assign_user=assign_user_item_dict,
        assign_length=assign_user_item_length,
        labeling_progress=assign_user_labeling_progress,
        labeling_flag=labeling_flag,
    ).save()

    # 创建一个task res表，将这个任务的结果存放起来
    for index, (question, answer) in enumerate(qa_list):
        await LabelResult(
            task_id=task_id,
            dataset_id=dataset_uid,
            creator="root",
            labeling_method=json_data["annotationTypes"],
            question_id=index + 1,
            question=question,
            answer=answer,
            status="未标注",
            assign_user=item_assign_user_dict[index],
        ).save()

    # 创建一个audit res表，存放审核结果
    audit_dict = {user["auditor"]: user["taskCount"] for user in json_data["auditAssignments"]}
    (
        item_audit_user_dict,
        audit_user_item_dict,
        audit_user_item_length,
        audit_progress,
    ) = distribute_audit_task(len(qa_list), audit_dict)
    audit_flag = {
        user: [False for _ in range(len(audit_user_item_dict[user]))]
        for user in audit_user_item_dict
    }
    # 生成Audit任务
    await AuditPage(
        task_id=task_id,
        end_time=json_data["deadline"],
        labeling_method=json_data["annotationTypes"],
        audit_user=audit_user_item_dict,
        audit_length=audit_user_item_length,
        audit_progress=audit_progress,
        audit_flag=audit_flag,
    ).save()
    # 插入数据，
    for index, (question, answer) in enumerate(qa_list):
        await AuditResult(
            task_id=task_id,
            status="未审核",
            question_id=index + 1,
            audit_user=item_audit_user_dict[index],
            question=question,
            answer=answer,
        ).save()

    return "success"


@router.get("/{resource}/get_datasets_name")
async def get_datasets_name(request: Request, resources=Depends(get_resources)):
    return ["test1", "test2"]


@router.get("/{resource}/get_user_list")
async def get_labeling_user_list(request: Request):
    admin_table = await Admin.all()
    user_list = [user.username for user in admin_table]
    return user_list
    # return {"user_list" : user_list }


# TODO, 这个位置是提供一个下载选项，将标注结果进行下载
@router.get("/{resource}/download/{pk}")
async def download_labeling_result(
    request: Request,
    pk: str = Path(...),
    model_resource: ModelResource = Depends(get_model_resource),
    resources=Depends(get_resources),
    model: Type[Model] = Depends(get_model),
):
    # 首先获取得到所有的标注结果，然后变成一个json数据返回给前端，前端完成数据的下载
    # 基于taskID进行过滤
    obj = await model.get(pk=pk).prefetch_related(*model_resource.get_m2m_field())
    # 获取得到对应task的id
    task_id = obj.task_id
    task_result = await LabelResult.filter(task_id=task_id).values(
        "question", "answer", "labeling_result"
    )
    # 这里添加数据装换操作
    # csv_data = convert_table_to_csv(task_result)
    # print(csv_data)
    return task_result
