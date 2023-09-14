from typing import Union

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from starlette.requests import Request

from dashboard.models import EvaluationPlan, ModelInfo, Record
from last.services.app import app
from last.services.depends import get_resources
from last.services.i18n import _
from last.services.template import templates

router = APIRouter()


class ModelView(BaseModel):
    endpoint: str
    access_key: str
    secret_key: str
    evaluation_plan: Union[str, None] = None


class EvalInfo(BaseModel):
    eval_plan_id: int
    model_id: int
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


@router.post("/evaluation/evaluation_create")
async def evaluation_create(
    eval_info: EvalInfo,
):
    plan = await EvaluationPlan.get_or_none(id=eval_info.eval_plan_id).values()
    model = await ModelInfo.get_or_none(id=eval_info.model_id).values()
    print(plan, model)
    await Record.create(
        eval_plan=plan["plan_name"],
        eval_plan_id=eval_info.eval_plan_id,
        model_name=model["name"],
        model_id=eval_info.model_id,
    )

    return {"status": "ok", "success": 1, "msg": "create eval success"}


# 用来创建model的接口
@router.post("/model/model_create")
async def create_model(request: Request, model_view: ModelView):
    # TODO: 这里需要根据endpoint地址去获取model的信息
    model_info = {
        "name": "书生·浦语",
        "model_type": "聊天机器人、自然语言处理助手",
        "version": "1.3.0",
        "base_model": "GShard-v2-xlarge",
    }
    await ModelInfo.create(
        name=model_info.name,
        endpoint=model_view.endpoint,
        access_key=model_view.access_key,
        secret_key=model_view.secret_key,
        model_type=model_info.model_type,
        version=model_info.version,
        base_model=model_info.base_model,
    )
    model_list = await ModelInfo.all().limit(10)
    eval_plans = await EvaluationPlan.all().limit(10)

    context = {
        "request": request,
        "eval_plans": eval_plans,
        "chosen_plan": model_view.evaluation_plan,
        "model_list": model_list,
    }
    return templates.TemplateResponse(
        "record/create_eval.html",
        context=context,
    )


# 用来获取model列表的接口
@router.get("/model/model_list")
async def get_model_list():
    try:
        model_list = await ModelInfo.all().values()
        return {"status": "ok", "success": 1, "data": model_list}
    except Exception as e:
        return {"status": "error", "success": 0, "msg": e}
