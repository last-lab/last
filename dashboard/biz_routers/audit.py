import ast
import html
from typing import Type

from fastapi import APIRouter, Depends, Path
from jinja2 import TemplateNotFound
from starlette.requests import Request
from tortoise import Model

from dashboard.biz_models import AuditPage, AuditResult, LabelResult
from last.services.depends import get_model, get_model_resource, get_resources
from last.services.resources import Model as ModelResource
from last.services.template import templates

router = APIRouter()


@router.get("/{resource}/audit/{pk}")
async def audit_view(
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
        # "labels": ast.literal_eval(request.query_params["audit_method"]),
    }
    # 点击了标注之后，需要根据传回来的参数，主要是数据集的名称，标注方式
    # 载入数据，丢一个新的界面出去
    try:
        return templates.TemplateResponse(
            f"{resource}/audit.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "audit.html",
            context=context,
        )


@router.get("/{resource}/revise")
async def revise_label_resut(request: Request, resource):
    context = {
        "request": request,
        "resource": resource,
        "labels": ast.literal_eval(request.query_params["audit_method"]),
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


@router.get("/{resource}/show_audit_data/{pk}")
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
            f"{resource}/audit_brief_dataset.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "audit_brief_dataset.html",
            context=context,
        )


@router.post("/{resource}/get_audit_data")
async def get_dataset_brief_from_db(request: Request, resource: str):
    # 插入审核的数据进来
    json_data = await request.json()
    task_id = json_data["taskID"]
    # 获取用户的id
    user_id = str(request.state.admin).split("#")[1]
    # 从审核结果表中找到对应的题，从labelresult表中得到标注后的结果，共同返回
    audit_results = await AuditResult.filter(task_id=task_id).values(
        "question_id", "question", "status", "audit_user"
    )
    # 从label result表中找到对应的标注结果
    label_results = await LabelResult.filter(task_id=task_id).values(
        "question_id", "answer", "status", "labeling_method"
    )
    res_list = []
    for audit_result, label_result in zip(audit_results, label_results):
        if user_id in audit_result["audit_user"]:
            # 只有题目是已经标注的情况下，这个题才算是能够进入到审核流程中
            if label_result["status"] != "未标注":
                res_list.append(
                    {
                        "question_id": audit_result["question_id"],
                        "question": audit_result["question"],
                        "status": audit_result["status"],
                        "action": "未审核" if audit_result["status"] != "已审核" else "查看",
                        "task_id": task_id,
                        "labeling_method": label_result["labeling_method"],
                    }
                )

    return res_list


@router.post("/{resource}/audit/{pk}/submit")
async def submit_callback(request: Request, resource: str, pk: str):
    user_id = str(request.state.admin).split("#")[1]
    json_data = await request.json()
    # TODO，对返回回来的结果进行处理，塞进LabelResult数据库中即可
    question_id = json_data["question_id"]
    task_id = json_data["task_id"]
    audit_result_by_user = json_data["auditResult"]
    audit_result_row = await AuditResult.filter(task_id=task_id, question_id=question_id)
    assert len(audit_result_row) == 1
    # 进行多人标注结果的合并  {'test1': res,} {'test1': res, 'test':res_2}
    audit_result = audit_result_row[0].audit_result
    # 将labelstudio的标注结果进行提取操作
    if audit_result is None:
        new_audit_result = {user_id: audit_result_by_user}
    else:
        # TODO 将新的标注结果和已经有的标注结果合并起来
        pass
    audit_result_row[0].audit_result = new_audit_result
    audit_result_row[0].status = "已审核"
    # TODO，暂时摆烂了，一个task的每一个题目只会到一个人手上
    await audit_result_row[0].save()
    # 修改一下auditpage的标注进展
    auditpage_row = await AuditPage.filter(task_id=task_id)
    assert len(auditpage_row) == 1
    current_audit_progress = eval(auditpage_row[0].audit_progress)
    current_audit_progress[user_id] += 1
    auditpage_row[0].audit_progress = current_audit_progress
    # 修改一下audit——flag
    audit_flag = eval(auditpage_row[0].audit_flag)
    audit_flag[user_id][int(question_id) - 1] = True
    auditpage_row[0].audit_flag = audit_flag
    await auditpage_row[0].save()
    # 需要修改一下labelresult中的状态，将对应的question的状态变成已审核
    label_result = await LabelResult.filter(task_id=task_id, question_id=question_id)
    label_result[0].status = "已审核"
    await label_result[0].save()


@router.post("/{resource}/audit/{pk}/update")
async def update_result_callback(request: Request, resource: str, pk: str):
    user_id = str(request.state.admin).split("#")[1]
    json_data = await request.json()
    question_id = json_data["question_id"]
    task_id = json_data["task_id"]
    update_audit_result = json_data["auditResult"]
    audit_row = await AuditResult.filter(task_id=task_id, question_id=question_id)
    assert len(audit_row) == 1
    # 进行多人标注结果的合并
    # audit_result = audit_row[0].audit_result
    # # 将labelstudio的标注结果进行提取操作
    # refine_audit_result = convert_labelstudio_result_to_string(audit_method, annotation)
    # 逻辑，如果当前user_id不在这个annotation中，就插入{'user_id': annotation}
    # assert audit_result is not None
    # TODO, 多用户同时更新需要进行修改
    update_result = {user_id: update_audit_result}
    audit_row[0].audit_result = update_result
    await audit_row[0].save()


# TODO eval --> json.loads()
@router.post("/{resource}/audit/next")
async def audit_next_callback(request: Request):
    user_id = str(request.state.admin).split("#")[1]
    json_data = await request.json()
    task_id = json_data["task_id"]
    current_question_index = json_data["current_question_index"]
    label_method = eval(html.unescape(json_data["labeling_method"]))
    # 从labelpage这个表中，基于user_id, question_id, task_id找到对应的记录
    auditpage_task_row = await AuditPage.filter(task_id=task_id)
    assert len(auditpage_task_row) == 1
    assign_user_item_list = eval(auditpage_task_row[0].audit_user)[user_id]
    assert current_question_index in assign_user_item_list
    # 获取current_question_index在assign_user_item_list中的索引
    index = assign_user_item_list.index(current_question_index)
    # 下一条标注的question_id
    next_question_index = assign_user_item_list[(index + 1) % len(assign_user_item_list)]
    # TODO 判断下一道题有没有被标注过，如果下一道题被标注了，就继续往下跳直到遇到False，或者回到最开始
    audit_flag = eval(auditpage_task_row[0].audit_flag)
    if audit_flag[user_id][next_question_index]:
        return {"question_id": "null", "task_id": task_id, "labeling_method": label_method}

    else:
        return {
            "question_id": next_question_index + 1,
            "task_id": task_id,
            "labeling_method": label_method,
        }


@router.post("/{resource}/get_audit_result")
async def get_audit_result(request: Request):
    user_id = str(request.state.admin).split("#")[1]
    json_data = await request.json()
    task_id = json_data["task_id"]
    question_id = json_data["question_id"]
    audit_result_row = await AuditResult.filter(task_id=task_id, question_id=question_id)
    audit_result = eval(audit_result_row[0].audit_result)
    return audit_result[user_id]
