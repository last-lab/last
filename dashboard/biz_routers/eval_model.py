import asyncio
import json
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from operator import add
from typing import Union

from fastapi import APIRouter, Depends, Path
from pydantic import BaseModel
from starlette.requests import Request
from tortoise.expressions import Q

from dashboard.biz_models import DataSet, EvaluationPlan, ModelInfo, Record, Risk
from dashboard.biz_models.eval_model import ModelRelateCase, ModelResult
from dashboard.constants import BASE_DIR
from dashboard.enums import EvalStatus
from dashboard.utils.converter import DataSetTool
from last.client import AI_eval, Client
from last.services.app import app
from last.services.depends import get_model_resource, get_resources
from last.services.i18n import _
from last.services.resources import Model as ModelResource
from last.services.template import templates

router = APIRouter()
executor = ThreadPoolExecutor()


# 创建模型Class
class ModelView(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    evaluation_plan: Union[str, None] = None


# 评测记录Class
class EvalInfo(BaseModel):
    plan_id: int
    llm_id: str
    llm_name: str
    created_at: int


# 评测结果Class
class ModelResultProp(BaseModel):
    record_id: int
    eval_type_id: int


# 创建评测的路由
@app.get("/record/add")
async def create_eval(
    request: Request,
    resources=Depends(get_resources),
):
    eval_plans = await EvaluationPlan.all().limit(50)
    model_list = await ModelInfo.all().limit(50)

    return templates.TemplateResponse(
        "record/create_eval.html",
        context={
            "request": request,
            "resources": resources,
            "resource_label": "Label",
            "page_pre_title": "BY LABEL STUDIO",
            "page_title": _("Create Evaluation"),
            "eval_plans": eval_plans,
            "model_list": model_list,
        },
    )


# TODO WangXunhong
async def client_execute(plan, record, dataset_info, AI_eval, kwargs_json):
    llm_name = json.loads(kwargs_json)["$llm_model"]["name"]
    _, new_dataset = await Client.execute(AI_eval, kwargs_json)  # 这里是计算逻辑，执行很慢
    # print("end")
    focused_risks = reduce(add, [dataset["focused_risks"] for dataset in dataset_info]).replace(
        "][", ","
    )
    result = await DataSet.create(
        name=plan["name"] + "+" + llm_name + "+问答记录",
        focused_risks=focused_risks,
        volume=new_dataset.volume,
        qa_num=new_dataset.qa_num,
        word_cnt=new_dataset.word_cnt,
        url=new_dataset.url,
        file=new_dataset.file,
        used_by=new_dataset.used_by,
        qa_records=str(new_dataset.qa_records),
        conversation_start_id=str(new_dataset.conversation_start_id),
        current_conversation_index=new_dataset.current_conversation_index,
        current_qa_record_id=new_dataset.current_qa_record_id,
        uid=new_dataset.uid,
        description=new_dataset.description,
        creator=str(new_dataset.creator),
        editor=new_dataset.editor,
        reviewer=new_dataset.reviewer,
        created_at=new_dataset.created_at,
        updated_at=new_dataset.created_at,
        permissions=new_dataset.permissions,
        first_risk_id="1",
    )
    # await compute_acc(plan, record, result, llm_name)
    await Record.filter(id=record.id).update(state=EvalStatus.finish)


# TODO compute_acc功能暂时还没写完 一些结果是mock的
async def compute_acc(plan, record, result, llm_name):
    score = await extract_score(result.qa_records)

    llm = await ModelInfo.get_or_none(name=llm_name)
    await ModelResult(
        record_id=record.id,
        eval_model_id=int(llm.id),
        eval_type_id=0,
        score=score,
    ).save()
    await ModelRelateCase(
        record_id=record,
        eval_model_id=int(llm.id),
        risk_type_id=1,
        score=score,
        come_dataset_id=1,
        content="2010年至2012年，北非和中东地区爆发了许多抗议活动，要求推翻腐败的政权，建立民主制度和保障基本的人权。…",
    ).save()


async def extract_score(string):
    pattern = r"评分：(\d+)"
    rating = re.findall(pattern, string)
    score = [int(r) for r in rating]
    return sum(score) / len(score)


# 创建评测记录接口


@router.post("/evaluation/evaluation_create")
async def evaluation_create(request: Request, eval_info: EvalInfo):  # TODO 加一个按钮，可以跳转查看评测结果的数据集
    plan = await EvaluationPlan.get_or_none(id=eval_info.plan_id).values()
    models = await ModelInfo.filter(
        Q(id__in=[int(x) for x in eval_info.llm_id.split(",")])
    ).values()
    record = await Record.create(
        eval_plan=plan["name"],
        plan_id=eval_info.plan_id,
        llm_name=eval_info.llm_name,
        llm_id=eval_info.llm_id,
        created_at=eval_info.created_at,
        created_user_id=str(request.state.admin).split("#")[1],
    )
    dataset_ids = [int(_) for _ in plan["dataset_ids"].split(",")]
    dataset_info = await DataSet.filter(Q(id__in=dataset_ids)).values()
    try:
        for model in models:
            kwargs_json = json.dumps(
                {
                    "$datasets": [
                        {
                            "name": dataset["name"],
                            "file": dataset["file"],
                            "focused_risks": dataset["focused_risks"],
                        }
                        for dataset in dataset_info
                    ],
                    "$llm_model": {
                        "name": model["name"],
                        "endpoint": model["endpoint"],
                        "access_key": model["access_key"],
                    },
                    "$critic_model": {
                        "name": models[0]["name"],
                        "endpoint": models[0]["endpoint"],
                        "access_key": models[0]["access_key"],
                    },
                    "$plan": {"name": plan["name"]},
                }
            )
            asyncio.create_task(client_execute(plan, record, dataset_info, AI_eval, kwargs_json))

    except Exception as e:
        await Record.filter(id=record.id).update(state=EvalStatus.error)
        return {"status": "error", "success": 0, "msg": str(e)}
    return {"status": "ok", "success": 1, "msg": "create eval success"}


# 用来创建model的接口
@router.post("/model/model_create")
async def create_model(model_view: ModelView):
    # TODO: @wangxuhong 写一个接口，输入是endpoint, AK, SK.
    # 输出是一个LLM类 类的定义 from last.types.llm import LLM
    model_info = {
        "name": f"{model_view.endpoint}",
        "model_type": "聊天机器人、自然语言处理助手",
        "version": "1.3.0",
        "base_model": "GShard-v2-xlarge",
        "parameter_volume": "约50亿个参数",
        "pretraining_info": "包含约7500亿个英文和中文字词的大规模无标签文本数据集",
        "finetuning_info": "通过Fine-tuning在任务特定数据集上进行微调",
        "alignment_info": "根据不同任务需求选择相应的数据集进行微调，如问答、摘要、机器翻译等任务",
    }
    await ModelInfo.create(
        name=model_info["name"],
        endpoint=model_view.endpoint,
        access_key=model_view.access_key,
        secret_key=model_view.secret_key,
        model_type=model_info["model_type"],
        version=model_info["version"],
        base_model=model_info["base_model"],
        parameter_volume=model_info["parameter_volume"],
        pretraining_info=model_info["pretraining_info"],
        finetuning_info=model_info["finetuning_info"],
        alignment_info=model_info["alignment_info"],
    )

    return {"status": "ok", "success": 1}


# 用来获取model列表的接口
@router.get("/model/model_list")
async def get_model_list():
    try:
        model_list = await ModelInfo.all().values()
        return {"status": "ok", "success": 1, "data": model_list}
    except Exception as e:
        return {"status": "error", "success": 0, "msg": e}


# 评测报告页面的路由
@router.get("/{resource}/report/{pk}")
async def get_report(
    request: Request,
    resource: str = Path(...),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
    pk: str = Path(...),
    page_size: int = 1,
    page_num: int = 1,
):
    # 评测方案信息
    base_info = await Record.get_or_none(id=pk).values()
    # 时间格式化
    time_array = time.localtime(base_info["created_at"] / 1000)
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    # 评测方案详情
    eval_plan = await EvaluationPlan.get_or_none(id=base_info["plan_id"])
    dataset_ids = eval_plan.dataset_ids.split(",")
    datasets = await DataSet.filter(id__in=dataset_ids)
    eval_type = "系统评分⭐"
    plan_content = eval_plan.dimensions.split(",")
    if eval_plan.eval_type == 1:
        eval_type = "人工评分 👤️"

    dataset_schema = await DataSetTool.ds_model_to_eval_model_schema(datasets)
    plan_detail = {
        "name": eval_plan.name,
        "score_way": eval_type,
        "plan_content": plan_content,
        "dataset_names": dataset_schema.dataset_names,
        "risk_detail": dataset_schema.risk_detail,
    }
    # risk
    risks_info = []
    risks = eval_plan.dimensions.split(",")
    for risk in risks:
        risk_name = risk.split("/")[0]
        risk_info = await Risk.get_or_none(risk_name=risk_name).values()
        risks_info.append(risk_info)
    # 典型风险案例
    risk_demos = await ModelRelateCase.all().filter(record_id=base_info["id"]).values()
    for demo in risk_demos:
        model = await ModelInfo.get_or_none(id=demo["eval_model_id"]).values()
        demo["eval_model_name"] = model["name"]
        risk = await Risk.get_or_none(id=demo["risk_type_id"]).values()
        demo["risk_type_name"] = risk["risk_name"]
        dataset = await DataSet.get_or_none(id=demo["come_dataset_id"]).values()
        demo["come_dataset_name"] = dataset["name"]

    total = len(risk_demos)

    return templates.TemplateResponse(
        f"{resource}/get_report.html",
        context={
            "request": request,
            "resource": resource,
            "resource_label": model_resource.label,
            "resources": resources,
            "model_resource": model_resource,
            "pk": pk,
            "page_title": _("模型评测报告"),
            "base_info": base_info,
            "format_time": format_time,
            "value": {"plan_detail": plan_detail},
            "risks_info": risks_info,
            "risk_demos": risk_demos,
            "page_num": page_num,
            "page_size": page_size,
            "total": total,
        },
    )


# 获取该记录的评测结果
@router.post("/{resource}/report/result")
async def get_result(request: Request, result: ModelResultProp):
    # 综合信息需获取该record_id下所有信息
    if result.eval_type_id == 0:
        results = await ModelResult.all().filter(record_id=result.record_id).values()
    else:
        # 维度信息还需要限制维度
        results = (
            await ModelResult.all()
            .filter(record_id=result.record_id, eval_type_id=result.eval_type_id)
            .values()
        )
    # 添加风险Name
    for item in results:
        model = await ModelInfo.get_or_none(id=item["eval_model_id"]).values()
        item["eval_model_name"] = model["name"]
        if item["eval_type_id"] == 0:
            item["eval_type_name"] = "综合评分"
        else:
            name = await Risk.get_or_none(id=item["eval_type_id"]).values()
            item["eval_type_name"] = name["risk_name"] + "评分"
            item["eval_data_set_score_json_list"] = json.loads(item["eval_data_set_score_json"])
            # 添加评测集名称
            for ele in item["eval_data_set_score_json_list"]:
                dataset_info = await DataSet.get_or_none(id=ele["id"]).values()
                ele["name"] = dataset_info["name"]
    return {"result": results}


# mk编辑页面的路由
@router.get("/{resource}/report/export/{pk}")
async def export(
    request: Request,
    resource: str = Path(...),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
    pk: str = Path(...),
):
    return templates.TemplateResponse(
        f"{resource}/report_edit.html",
        context={
            "request": request,
            "resource": resource,
            "resource_label": model_resource.label,
            "resources": resources,
            "model_resource": model_resource,
            "pk": pk,
            "page_title": _("模型评测报告编辑"),
        },
    )


class ISaveInit(BaseModel):
    url: str


# 获取初始md内容
@router.post("/{resource}/report/read")
async def read_md(request: Request, data: ISaveInit):
    file_init = os.path.join(BASE_DIR, "static", "mdSave", data.url)
    # 判断是否存在保存的md
    if os.path.exists(file_init):
        file_path = file_init
    else:
        # init.md为mock的初始md
        file_path = os.path.join(BASE_DIR, "static", "mdSave", "init.md")
    file = open(file_path, "r", encoding="utf-8")
    line = file.readlines()
    return line


class ISave(BaseModel):
    name: str
    content: str


# 导出之后保存操作和清除操作
@router.post("/{resource}/report/save")
async def save_pdf(request: Request, data: ISave):
    # TODO 导出的md文件暂时保存在/static/mdSave中
    file_path = os.path.join(BASE_DIR, "static", "mdSave", data.name)
    file_handle = open(file_path, "w", encoding="utf-8")
    file_handle.write(data.content)
    file_handle.close()
    # TODO 导出之后，删除之前保存在/static/mdSave的文件
    file_exist = os.path.join(BASE_DIR, "static", "mdSave", data.name)
    if os.path.exists(file_exist):
        os.remove(file_exist)
    return {"mes": 1}


# 保存操作
@router.post("/{resource}/report/save/md")
async def save_md(request: Request, data: ISave):
    # TODO 保存的md文件暂时保存在/static/mdSave中
    file_path = os.path.join(BASE_DIR, "static", "mdSave", data.name)
    file_handle = open(file_path, "w", encoding="utf-8")
    file_handle.write(data.content)
    file_handle.close()
    return {"mes": 1}
