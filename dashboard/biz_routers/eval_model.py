import json
from concurrent.futures import ThreadPoolExecutor
from functools import reduce
from operator import add
from typing import Union

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.requests import Request
from tortoise.expressions import Q

from dashboard.biz_models import DataSet, EvaluationPlan, ModelInfo, Record
from dashboard.enums import EvalStatus
from last.client import AI_eval, Client
from last.services.app import app
from last.services.depends import get_resources
from last.services.i18n import _
from last.services.template import templates

router = APIRouter()
executor = ThreadPoolExecutor()


class ModelView(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    evaluation_plan: Union[str, None] = None


class EvalInfo(BaseModel):
    plan_id: int
    llm_id: int
    created_at: str


@app.get("/record/add")
async def create_eval(
    request: Request,
    resources=Depends(get_resources),
):
    eval_plans = await EvaluationPlan.all().limit(10)
    model_list = await ModelInfo.all().limit(10)

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


async def client_execute(plan, record, dataset_info, AI_eval, kwargs_json):
    # await asyncio.sleep(10)
    print("kaishi")
    _, new_dataset = await Client.execute(AI_eval, kwargs_json)  # 这里是计算逻辑，执行很慢
    print("wancheng")
    focused_risks = reduce(add, [dataset["focused_risks"] for dataset in dataset_info]).replace(
        "][", ","
    )
    await DataSet.create(
        name=plan["name"] + "_Result",
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
        first_risk_id="1",  # 这里的逻辑不正确，TODO 改掉
    )
    await Record.filter(id=record.id).update(state=EvalStatus.finish)


@router.post("/evaluation/evaluation_create")
async def evaluation_create(eval_info: EvalInfo):
    plan = await EvaluationPlan.get_or_none(id=eval_info.plan_id).values()
    model = await ModelInfo.get_or_none(id=eval_info.llm_id).values()
    record = await Record.create(
        eval_plan=plan["name"],
        plan_id=eval_info.plan_id,
        llm_name=model["name"],
        llm_id=eval_info.llm_id,
    )
    # try:
    dataset_ids = [int(_) for _ in plan["dataset_ids"].split(",")]
    dataset_info = await DataSet.filter(Q(id__in=dataset_ids)).values()
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
                "name": model["name"],
                "endpoint": model["endpoint"],
                "access_key": model["access_key"],
            },
            "$plan": {"name": plan["name"]},
        }
    )
    try:
        await client_execute(plan, record, dataset_info, AI_eval, kwargs_json)
        return {"status": "ok", "success": 1, "msg": "create eval success"}
    except Exception as e:
        return {"status": "error", "success": 0, "msg": str(e)}
    

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
