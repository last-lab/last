import ast
import html
from typing import Type

from fastapi import APIRouter, Depends, Path
from jinja2 import TemplateNotFound
from starlette.requests import Request
from tortoise import Model

from dashboard.biz_models import AuditPage, AuditResult, LabelResult
from dashboard.tools.statistic import convert_audit_data, convert_data_to_labelstudio_data
from last.services.depends import get_model, get_model_resource, get_resources
from last.services.resources import Model as ModelResource
from last.services.template import templates

router = APIRouter()


@router.get("/{resource}/audit/{pk}")
async def audit_view(
    request: Request,
    resource: str = Path(...),
    pk: str = Path(...),
    model_resource: ModelResource = Depends(get_model_resource),
    resources=Depends(get_resources),
    model: Type[Model] = Depends(get_model),
):
    # TODO 标注方法从数据库中读取出来，或者直接在brief_dataset页面直接传
    task_pk_value = request.query_params["task_pk_value"]
    context = {
        "request": request,
        "resource": resource,
        "pk": pk,
        "task_pk_value": task_pk_value,
        "labels": ast.literal_eval(request.query_params["labeling_method"]),
        "risk_level": request.query_params["risk_level"],
        "model_resource": model_resource,
        "resources": resources,
        "selected_list_string": request.query_params["selected_list_string"],
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


@router.get("/{resource}/revise/{pk}")
async def revise_label_resut(request: Request, resource):
    context = {
        "request": request,
        "resource": resource,
        "labels": ast.literal_eval(request.query_params["labeling_method"]),
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
        "question_id", "question", "answer", "status", "audit_user", "model_label", "model_reason"
    )
    # 从label result表中找到对应的标注结果
    label_results = await LabelResult.filter(task_id=task_id).values(
        "question_id", "answer", "status", "labeling_method", "risk_level"
    )
    res_list = []
    for audit_result, label_result in zip(audit_results, label_results):
        if user_id in eval(audit_result["audit_user"]):
            # 只有题目是已经标注的情况下，这个题才算是能够进入到审核流程中
            if label_result["status"] != "未标注":
                res_list.append(
                    {
                        "question_id": audit_result["question_id"],
                        "question": audit_result["question"],
                        "answer": audit_result["answer"],
                        "model_label": audit_result["model_label"],
                        "model_reason": audit_result["model_reason"],
                        "status": audit_result["status"],
                        "action": "审核" if "已审核" not in audit_result["status"] else "查看",
                        "task_id": task_id,
                        "labeling_method": label_result["labeling_method"],
                        "risk_level": label_result["risk_level"],
                        "label_status": label_result["status"],
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
    labeling_method = json_data["labeling_method"]
    risk_level = json_data["risk_level"]
    audit_result_row = await AuditResult.filter(task_id=task_id, question_id=question_id)
    assert len(audit_result_row) == 1
    # 进行多人标注结果的合并  {'test1': res,} {'test1': res, 'test':res_2}
    audit_result = audit_result_row[0].audit_result
    audit_result_by_user = convert_audit_data(labeling_method, audit_result_by_user, risk_level)
    # 将labelstudio的标注结果进行提取操作
    if audit_result is None:
        new_audit_result = {user_id: audit_result_by_user}
    else:
        # TODO 将新的标注结果和已经有的标注结果合并起来
        new_audit_result = {user_id: audit_result_by_user}
    audit_result_row[0].audit_result = new_audit_result
    audit_flag = json_data["auditFlag"]
    audit_result_row[0].status = "已审核_" + audit_flag
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
    audit_user = eval(auditpage_row[0].audit_user)[user_id]  # [1,3,6]
    audit_item_index = audit_user.index(int(question_id) - 1)  # 获取audit问题在审核者中的索引
    audit_flag[user_id][audit_item_index] = True
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
    update_audit_flag = json_data["auditFlag"]
    labeling_method = json_data["labeling_method"]
    risk_level = json_data["risk_level"]
    update_audit_result = convert_audit_data(labeling_method, update_audit_result, risk_level)
    # audit_flag = json_data["auditFlag"]
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
    audit_row[0].status = "已审核_" + update_audit_flag
    await audit_row[0].save()


# TODO eval --> json.loads()
@router.post("/{resource}/audit/next")
async def audit_next_callback(request: Request):
    user_id = str(request.state.admin).split("#")[1]
    json_data = await request.json()
    task_id = json_data["task_id"]
    current_question_index = json_data["current_question_index"]
    label_method = eval(html.unescape(json_data["labeling_method"]))
    # filter_dict = eval(json_data["filter"]) # {"model_label": '4'} / None /
    risk_level = json_data["risk_level"]
    search_index_list = [
        int(element) - 1 for element in json_data["selected_list_string"].split(",")
    ]
    # audit_item = await AuditResult.filter(task_id=task_id, **filter_dict, status="未审核")
    # 从labelpage这个表中，基于user_id, question_id, task_id找到对应的记录
    auditpage_task_row = await AuditPage.filter(task_id=task_id)
    audit_user_item_list = eval(auditpage_task_row[0].audit_user)[user_id]
    audit_flag = eval(auditpage_task_row[0].audit_flag)
    # 获取current_question_index在assign_user_item_list中的索引
    next_element = None
    if len(search_index_list) == 1:
        next_flag = False
    else:
        next_flag = False
        for element in search_index_list:
            if (element) != current_question_index:
                search_item_index = audit_user_item_list.index(element)
                if not audit_flag[user_id][search_item_index]:
                    next_flag = True
                    next_element = element
                    break

    if next_flag:
        return {
            "question_id": next_element + 1,
            "task_id": task_id,
            "labeling_method": label_method,
            "risk_level": risk_level,
        }

    else:
        return {
            "question_id": "null",
            "task_id": task_id,
            "labeling_method": label_method,
            "risk_level": risk_level,
        }


@router.post("/{resource}/get_audit_result")
async def get_audit_result(request: Request):
    # user_id = str(request.state.admin).split("#")[1]
    json_data = await request.json()
    task_id = json_data["task_id"]
    question_id = json_data["question_id"]
    audit_result_row = await AuditResult.filter(task_id=task_id, question_id=question_id)
    status = audit_result_row[0].status
    # audit_result = eval(audit_result_row[0].audit_result)
    return status.split("_")[-1]


@router.post("/{resource}/audit/get_config")
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
    data = await AuditResult.filter(task_id=task_id, question_id=question_id)
    risk_level_dict = {"1": "高度敏感", "2": "中度敏感", "3": "低度敏感", "4": "中性词"}
    # 将下一个题目的id也返回回去，如果这个标注已经结束了，值就用null返回
    assert len(data) == 1
    labeling_method = json_data["labeling_method"]
    # 查找出来标注方法，根据不同的标注方法定义不同的返回结果,如answer字段
    query_data = {
        "Q": data[0].question,
        "A": data[0].answer,
        "labeling_method": labeling_method,
        "user_id": user_id,
    }

    if "Model" in query_data["labeling_method"]:
        if data[0].model_label == "nan":
            query_data["model_label"] = "None"
        else:
            query_data["model_label"] = risk_level_dict[data[0].model_label]

        query_data["model_reason"] = data[0].model_reason

    else:
        query_data["model_label"] = "None"
        query_data["model_reason"] = "None"
    return query_data


@router.post("/{resource}/audit/get_data")
async def get_annotatoin_and_predict_data(request: Request, resource: str):
    """_summary_
    # 需要返回labelstudio需要的annotation和predict的两个数据

    Args:
        request (Request): _description_
        resource (str): _description_
    """
    mock_data = {"annotations": [], "predictions": []}
    return mock_data


@router.post("/{resource}/audit/get_label_result")
async def get_label_reset(request: Request, resource: str):
    json_data = await request.json()
    task_id = json_data["task_id"]
    question_id = json_data["question_id"]
    labeling_method = json_data["labeling_method"]
    # 查找数据结果表，得到标注结果
    data = await LabelResult.filter(task_id=task_id, question_id=question_id)
    raw_labeling_result = data[0].raw_labeling_result
    # 如果是使用model标注，则直接构造一个结果返回
    if raw_labeling_result is not None:
        return raw_labeling_result
    else:
        if "Model" in labeling_method:
            data = await AuditResult.filter(task_id=task_id, question_id=question_id)
            risk_level_dict = {"1": "高度敏感", "2": "中度敏感", "3": "低度敏感", "4": "中性词"}
            if data[0].model_label == "nan":
                model_label = ""
            else:
                model_label = risk_level_dict[data[0].model_label]
            return (
                "[{'value': {'choices': ['"
                + model_label
                + "']}, 'id': 'ONWk5-qNZn', 'from_name': 'rating', 'to_name': 'risk_dialog', 'type': 'choices', 'origin': 'manual'}]"
            )
    return raw_labeling_result


@router.post("/{resource}/audit/get_revise_label_result")
async def get_revise_label_result(request: Request, resource: str):
    # 这个函数是和上面这个函数相对，只用于审核revise页面的函数
    json_data = await request.json()
    user_id = str(request.state.admin).split("#")[1]
    task_id = json_data["task_id"]
    question_id = json_data["question_id"]
    # labeling_method = json_data["labeling_method"]
    # 返回的是一个{"test": {"风险程度": 1}}之类的二级字典，现在需要重新变成一个labelstudio类型的数据
    labeling_data = await LabelResult.filter(task_id=task_id, question_id=question_id)
    # 将这个标注结果数据和审核数据一起送入到转换函数中
    audit_data = await AuditResult.filter(task_id=task_id, question_id=question_id)
    if labeling_data[0].raw_labeling_result is not None:
        audit_labeled_data = convert_data_to_labelstudio_data(
            eval(labeling_data[0].raw_labeling_result), eval(audit_data[0].audit_result)[user_id]
        )
    else:
        audit_labeled_data = convert_data_to_labelstudio_data(
            None, eval(audit_data[0].audit_result)[user_id]
        )
    return audit_labeled_data
