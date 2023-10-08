import ast
from typing import Type

from fastapi import APIRouter, Depends, Path
from jinja2 import TemplateNotFound
from starlette.requests import Request
from tortoise import Model

from dashboard.biz_models import LabelResult
from last.services.depends import get_model, get_model_resource, get_resources
from last.services.resources import Model as ModelResource
from last.services.template import templates

router = APIRouter()


@router.get("/{resource}/labeling/{pk}")
async def labeling_view(
    request: Request,
    resource: str = Path(...),
    pk: str = Path(...),
):
    # TODO 标注方法从数据库中读取出来，或者直接在brief_dataset页面直接传

    context = {
        "request": request,
        "resource": resource,
        "pk": pk,
        "labels": ast.literal_eval(request.query_params["labeling_method"]),
    }
    # 点击了标注之后，需要根据传回来的参数，主要是数据集的名称，标注方式
    # 载入数据，丢一个新的界面出去
    print(context)
    try:
        return templates.TemplateResponse(
            f"{resource}/label.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "label.html",
            context=context,
        )


@router.get("/{resource}/display/{pk}")
async def display(
    request: Request,
    resource: str = Path(...),
    pk: str = Path(...),
    model_resource: ModelResource = Depends(get_model_resource),
    resources=Depends(get_resources),
    model: Type[Model] = Depends(get_model),
):
    obj = await model.get(pk=pk).prefetch_related(*model_resource.get_m2m_field())
    # 获取得到对应task的id
    task_id = obj.task_id
    labeling_method = obj.labeling_method
    context = {
        "request": request,
        "resources": resources,
        "resource_label": model_resource.label,
        "resource": resource,
        "pk": pk,
        "model_resource": model_resource,
        "page_title": model_resource.page_title,
        "page_pre_title": model_resource.page_pre_title,
        "task_id": task_id,
        "labeling_method": labeling_method,
    }
    try:
        return templates.TemplateResponse(
            f"{resource}/brief_dataset.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "brief_dataset.html",
            context=context,
        )


@router.post("/{resource}/get_dataset_brief_data")
async def get_dataset_brief_from_db(request: Request, resource: str):
    # 需要有task id的名字，然后根据这个名字从task table中获取得到对应的dataset的名字
    # 再从dataset表中取出来dataset的文件路径
    # 读取这个文件的路径获取得到文件的数据

    json_data = await request.json()
    task_id = json_data["taskID"]
    # 从result表中获取所有的question字段的结果
    # 获取result表中给定task_id的所有记录
    results = await LabelResult.filter(task_id=task_id).values(
        "question_id", "question", "status", "labeling_method"
    )
    res_list = []
    for result in results:
        res_list.append(
            {
                "question_id": result["question_id"],
                "question": result["question"],
                "status": result["status"],
                "action": "标注" if result["status"] == "未标注" else "查看",
                "task_id": task_id,
                "labeling_method": result["labeling_method"],
            }
        )

    return res_list


@router.post("/{resource}/labeling/get_config")
async def get_config_from_db(request: Request, resource: str):
    """_summary_
    # 需要返回 id，支持数据库的搜索

    Args:
        request (Request): _description_
        resource (str): _description_
    """
    json_data = await request.json()
    task_id = json_data["task_id"]
    question_id = json_data["question_id"]
    # 查找默认得到一个列表，尽管只有一个元素
    data = await LabelResult.filter(task_id=task_id, question_id=question_id)
    assert len(data) == 1
    labeling_method = data[0].labeling_method
    # 查找出来标注方法，根据不同的标注方法定义不同的返回结果,如answer字段
    query_data = {"Q": data[0].question, "A": data[0].answer, "labeling_method": labeling_method}
    return query_data


@router.post("/{resource}/labeling/get_data")
async def get_annotatoin_and_predict_data(request: Request, resource: str):
    """_summary_
    # 需要返回labelstudio需要的annotation和predict的两个数据

    Args:
        request (Request): _description_
        resource (str): _description_
    """
    mock_data = {"annotations": [], "predictions": []}
    return mock_data


@router.post("/{resource}/labeling/{pk}/submit")
async def submit_callback(request: Request, resource: str, pk: str):
    json_data = await request.json()
    # TODO，对返回回来的结果进行处理，塞进LabelResult数据库中即可
    question_id = json_data["question_id"]
    task_id = json_data["task_id"]
    annotation = json_data["annotation"]
    labeling_row = await LabelResult.filter(task_id=task_id, question_id=question_id)
    assert len(labeling_row) == 1
    labeling_row[0].labeling_result = annotation
    labeling_row[0].status = "标注完成"
    await labeling_row[0].save()
    # 修改task表中这一条数据的状态
    print(json_data)
