from typing import Union

from fastapi import APIRouter
from pydantic import BaseModel

from dashboard.models import ModelInfo, EvaluationPlan
from dashboard.widgets.displays import ShowModelCard
from last.services.template import templates
from starlette.requests import Request

router = APIRouter()


class ModelView(BaseModel):
    name: str
    model_ak: str
    model_sk: str
    evaluation_plan: Union[str, None] = None


# 用来创建model的接口
@router.post("/model/model_create")
async def create_model(
    request: Request,
    model_view: ModelView
):
    await ModelInfo.create(name=model_view.name, access_key=model_view.model_ak, secret_key=model_view.model_sk)
    model_list = await ModelInfo.all().limit(10)
    eval_plans = await EvaluationPlan.all().limit(10)
    model_cards = []
    for model_detail in model_list:
        card = await ShowModelCard().render(request, model_detail)
        model_cards.append(card)

    context = {
        "request": request,
        "eval_plans": eval_plans,
        "chosen_plan": model_view.evaluation_plan,
        "model_cards": model_cards,
    }
    return templates.TemplateResponse(
        "create_eval.html",
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
