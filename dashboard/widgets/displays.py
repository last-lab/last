import json
from ast import literal_eval

from starlette.requests import Request

from dashboard.biz_models import DataSet, EvaluationPlan, ModelInfo
from dashboard.enums import EvalStatus
from last.services.widgets.displays import Display, Popover, Status
from dashboard.utils.converter import DataSetTool


class ShowIp(Display):
    async def render(self, request: Request, value: str):
        if value:
            items = value.split(".")
            value = ".".join([items[0], items[1], "*", "*"])
        return await super().render(request, value)


class ShowStatus(Status):
    async def render(self, request: Request, value: str):
        color = ""
        text = ""
        if value == EvalStatus.on_progress:
            color = "status-green"
            text = "On Progress"
        elif value == EvalStatus.finish:
            color = "status-black"
            text = "Finished"
        elif value == EvalStatus.error:
            color = "status-red"
            text = "Error"
        elif value == EvalStatus.un_labeled:
            color = "status-yellow"
            text = "Unlabeled"
        return await super().render(request, {"color": color, "text": text})


class ShowPopover(Popover):
    async def render(self, request: Request, value: str):
        return await super().render(
            request, {"content": value, "popover": value, "title": "Detail"}
        )


class ShowPlanDetail(Display):
    template = "record/record_plan_modal.html"

    async def render(self, request: Request, value: str):
        eval_plan = await EvaluationPlan.get_or_none(id=value)
        dataset_ids = eval_plan.dataset_ids.split(",")
        datasets = await DataSet.filter(id__in=dataset_ids)
        dataset_names = []
        risk_details = []
        eval_type = '系统评分⭐'
        if eval_plan.eval_type == 1:
            eval_type = "人工评分 👤️"

        for ds in datasets:
            dataset_names.append(ds.name)
            risk_details.append(json.loads(ds.dimensions))

        risk_names = []
        for r in risk_details:
            if isinstance(r, list):
                for r_item in r:
                    risk_names.append(r_item['name'])
            else:
                risk_names.append(r['name'])

        plan_detail = {
            "name": eval_plan.name,
            "score_way": eval_type,
            "plan_content": eval_plan.dimensions,
            "dataset_names": "\n".join(dataset_names),
            "risk_detail": "\n".join(risk_names),
        }

        return await super().render(
            request,
            {"plan_detail": plan_detail},
        )


class ShowOperation(Display):
    template = "record/record_operations.html"

    async def render(self, request: Request, value: int):
        model_detail = await ModelInfo.get_or_none(id=value).values()
        # TODO: 下面的 record_file 需要替换为查询得到文件列表
        record_file = ["书生·浦语 1.3.0", "送评模型1 1.0", "送评模型1 1.4"]
        return await super().render(
            request,
            {
                "model_detail": model_detail,
                "record_file": record_file,
            },
        )


class ShowModelCard(Display):
    template = "record/model_card.html"

    async def render(self, request: Request, value: str):
        return await super().render(
            request,
            {
                "model_detail": value,
            },
        )


class ShowAction(Display):
    template = "dataset/action_dataset.html"

    async def render(self, request: Request, value: any):
        dataset = {}
        label = []
        if value is not None:
            dataset = await DataSet.get(id=value).values()
            label = literal_eval(dataset["focused_risks"])
        return await super().render(request, {**dataset, "focused_risks": label})


class ShowRiskType(Display):
    template = "dataset/risk.html"

    async def render(self, request: Request, value: any):
        label = list(filter(lambda x: x["level"] == 1, literal_eval(value)))
        return await super().render(request, {"content": label})


class ShowSecondType(Display):
    template = "dataset/risk_second.html"

    async def render(self, request: Request, value: any):
        label = list(filter(lambda x: x["level"] == 2, literal_eval(value)))
        return await super().render(
            request,
            {
                "content": ",".join([d["name"] for d in label]),
                "popover": ",".join([d["name"] for d in label]),
            },
        )
