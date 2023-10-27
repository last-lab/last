import ast
import html
from typing import Type

from fastapi import APIRouter, Depends, Path
from jinja2 import TemplateNotFound
from starlette.requests import Request
from tortoise import Model

from dashboard.biz_models import LabelPage, LabelResult
from dashboard.tools.statistic import (
    concat_aduit_result,
    convert_labelstudio_result_to_string,
    update_aduit_result,
)
from last.services.depends import get_model, get_model_resource, get_resources
from last.services.resources import Model as ModelResource
from last.services.template import templates

router = APIRouter()


@router.get("/{resource}/aduit/{pk}")
async def aduit_view(
    request: Request,
    resource: str = Path(...),
    pk: str = Path(...),
):
    # TODO 标注方法从数据库中读取出来，或者直接在brief_dataset页面直接传
    task_pk_value = request.query_params["task_pk_value"]
    context = {
        "request": request,
        "resource": resource,
        "pk": pk,
        "task_pk_value": task_pk_value,
        "labels": ["判断标注"],
        # "labels": ast.literal_eval(request.query_params["aduit_method"]),
    }
    # 点击了标注之后，需要根据传回来的参数，主要是数据集的名称，标注方式
    # 载入数据，丢一个新的界面出去
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


@router.get("/{resource}/revise")
async def revise_label_resut(request: Request, resource):
    context = {
        "request": request,
        "resource": resource,
        "labels": ast.literal_eval(request.query_params["aduit_method"]),
    }
    try:
        return templates.TemplateResponse(
            f"{resource}/revise.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "revise.html",
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
    aduit_method = obj.aduit_method

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
        "aduit_method": aduit_method,
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
    # 获取用户的id
    user_id = str(request.state.admin).split("#")[1]
    # 从result表中获取所有的question字段的结果
    # 获取result表中给定task_id的所有记录
    results = await LabelResult.filter(task_id=task_id).values(
        "question_id", "question", "status", "aduit_method", "assign_user"
    )
    res_list = []
    for result in results:
        if user_id in result["assign_user"]:
            res_list.append(
                {
                    "question_id": result["question_id"],
                    "question": result["question"],
                    "status": result["status"],
                    "action": "标注" if result["status"] == "未标注" else "查看",
                    "task_id": task_id,
                    "aduit_method": result["aduit_method"],
                }
            )

    return res_list


@router.post("/{resource}/aduit/get_config")
async def get_config_from_db(request: Request, resource: str):
    """_summary_
    # 需要返回 id，支持数据库的搜索

    Args:
        request (Request): _description_
        resource (str): _description_
    """
    user_id = str(request.state.admin).split("#")[1]
    json_data = await request.json()
    task_id = json_data["task_id"]
    question_id = json_data["question_id"]
    # 查找默认得到一个列表，尽管只有一个元素
    data = await LabelResult.filter(task_id=task_id, question_id=question_id)
    # 将下一个题目的id也返回回去，如果这个标注已经结束了，值就用null返回
    assert len(data) == 1
    aduit_method = data[0].aduit_method
    # 查找出来标注方法，根据不同的标注方法定义不同的返回结果,如answer字段
    query_data = {
        "Q": data[0].question,
        "A": data[0].answer,
        "aduit_method": aduit_method,
        "user_id": user_id,
    }
    return query_data


@router.post("/{resource}/aduit/get_data")
async def get_annotatoin_and_predict_data(request: Request, resource: str):
    """_summary_
    # 需要返回labelstudio需要的annotation和predict的两个数据

    Args:
        request (Request): _description_
        resource (str): _description_
    """
    mock_data = {"annotations": [], "predictions": []}
    return mock_data


@router.post("/{resource}/aduit/get_label_result")
async def get_label_reset(request: Request, resource: str):
    json_data = await request.json()
    task_id = json_data["task_id"]
    question_id = json_data["question_id"]
    # 查找数据结果表，得到标注结果
    data = await LabelResult.filter(task_id=task_id, question_id=question_id)
    raw_aduit_result = data[0].raw_aduit_result
    return raw_aduit_result


@router.post("/{resource}/aduit/{pk}/submit")
async def submit_callback(request: Request, resource: str, pk: str):
    user_id = str(request.state.admin).split("#")[1]
    json_data = await request.json()
    # TODO，对返回回来的结果进行处理，塞进LabelResult数据库中即可
    question_id = json_data["question_id"]
    task_id = json_data["task_id"]
    annotation = json_data["annotation"]
    aduit_method = json_data["aduit_method"]
    aduit_row = await LabelResult.filter(task_id=task_id, question_id=question_id)
    assert len(aduit_row) == 1
    # 进行多人标注结果的合并
    aduit_result = aduit_row[0].aduit_result
    # 将labelstudio的标注结果进行提取操作
    refine_aduit_result = convert_labelstudio_result_to_string(aduit_method, annotation)
    # 逻辑，如果当前user_id不在这个annotation中，就插入{'user_id': annotation}
    if aduit_result is None:
        new_aduit_result = {user_id: refine_aduit_result}
    else:
        # 将新的标注结果和已经有的标注结果合并起来
        new_aduit_result = concat_aduit_result(
            user_id, refine_aduit_result, aduit_result
        )
    aduit_row[0].aduit_result = new_aduit_result
    aduit_row[0].status = "标注完成"
    # TODO，暂时摆烂了，一个task的每一个题目只会到一个人手上
    aduit_row[0].raw_aduit_result = annotation
    await aduit_row[0].save()
    # 修改一下标注进展
    labelpage_row = await LabelPage.filter(task_id=task_id)
    assert len(labelpage_row) == 1
    current_aduit_progress = eval(labelpage_row[0].aduit_progress)
    current_aduit_progress[user_id] += 1
    labelpage_row[0].aduit_progress = current_aduit_progress
    # 修改一下aduit_flag
    aduit_flag = eval(labelpage_row[0].aduit_flag)
    aduit_flag[user_id][int(question_id) - 1] = True
    labelpage_row[0].aduit_flag = aduit_flag
    await labelpage_row[0].save()


@router.post("/{resource}/aduit/{pk}/update")
async def update_result_callback(request: Request, resource: str, pk: str):
    user_id = str(request.state.admin).split("#")[1]
    json_data = await request.json()
    question_id = json_data["question_id"]
    task_id = json_data["task_id"]
    annotation = json_data["annotation"]
    aduit_method = json_data["aduit_method"]
    aduit_row = await LabelResult.filter(task_id=task_id, question_id=question_id)
    assert len(aduit_row) == 1
    # 进行多人标注结果的合并
    aduit_result = aduit_row[0].aduit_result
    # 将labelstudio的标注结果进行提取操作
    refine_aduit_result = convert_labelstudio_result_to_string(aduit_method, annotation)
    # 逻辑，如果当前user_id不在这个annotation中，就插入{'user_id': annotation}
    assert aduit_result is not None
    # 更新已经有的结果
    update_result = update_aduit_result(user_id, refine_aduit_result, aduit_result)
    aduit_row[0].aduit_result = update_result
    aduit_row[0].raw_aduit_result = annotation
    await aduit_row[0].save()


@router.post("/{resource}/aduit/next")
async def aduit_next_callback(request: Request):
    user_id = str(request.state.admin).split("#")[1]
    json_data = await request.json()
    task_id = json_data["task_id"]
    current_question_index = json_data["current_question_index"]
    aduit_method = eval(html.unescape(json_data["aduit_method"]))
    # 从labelpage这个表中，基于user_id, question_id, task_id找到对应的记录
    labelpage_task_row = await LabelPage.filter(task_id=task_id)
    assert len(labelpage_task_row) == 1
    assign_user_item_list = ast.literal_eval(labelpage_task_row[0].assign_user)[user_id]
    assert current_question_index in assign_user_item_list
    # 获取current_question_index在assign_user_item_list中的索引
    index = assign_user_item_list.index(current_question_index)
    # 下一条标注的question_id
    next_question_index = assign_user_item_list[(index + 1) % len(assign_user_item_list)]
    # TODO 判断下一道题有没有被标注过，如果下一道题被标注了，就继续往下跳直到遇到False，或者回到最开始
    aduit_flag = eval(labelpage_task_row[0].aduit_flag)
    if aduit_flag[user_id][next_question_index]:
        return {"question_id": "null", "task_id": task_id, "aduit_method": aduit_method}

    else:
        return {
            "question_id": next_question_index + 1,
            "task_id": task_id,
            "aduit_method": aduit_method,
        }


@router.post("/{resource}/aduit/get_label_audit_status")
async def get_label_audit_status(request: Request):
    json_data = await request.json()
    task_id = json_data["task_id"]
    question_id = json_data["question_id"]
    # 查找数据结果表，得到标注结果
    data = await LabelResult.filter(task_id=task_id, question_id=question_id)
    data_status = data[0].status
    if data_status == "已审核":
        return True
    else:
        return False
