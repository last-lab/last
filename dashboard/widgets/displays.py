import json

from starlette.requests import Request

from dashboard.biz_models import DataSet, EvaluationPlan, ModelInfo
from dashboard.enums import EvalStatus
from last.services.widgets.displays import Display, Popover, Status


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

        for ds in datasets:
            dataset_names.append(ds.name)
            risk_details.append(json.loads(ds.dimensions))

        plan_detail = {
            "name": eval_plan.name,
            "score_way": eval_plan.eval_type,
            "plan_content": eval_plan.dimensions,
            "dataset_names": dataset_names,
            "risk_detail": risk_details,
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
        return await super().render(
            request,
            {
                "detail": {
                    "id": "1",
                    "name": "评测集1",
                    "type": "国家安全",
                    "moreType": [
                        {"subType": "颠覆国家政权", "thirdType": ["三级维度1", "三级维度2"]},
                        {"subType": "宣传恐怖主义", "thirdType": ["三级维度3", "三级维度4"]},
                    ],
                    "url": "C://Users/fanhao/Desktop/large-language-all-table.json",
                    "dataCount": 666,
                    "number": 10000,
                    "size": "10.6GB",
                    "updateTime": "2022-11-08 19:00:00",
                    "useCount": 100,
                },
                "dataset_file": {"content": "content", "word": "word"},
            },
        )
