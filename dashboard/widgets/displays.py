from ast import literal_eval

from starlette.requests import Request

from dashboard.enums import EvalStatus
from dashboard.models import DataSet
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


class ShowOperation(Display):
    template = "widgets/record_operations.html"

    async def render(self, request: Request, value: str):
        return await super().render(
            request,
            {
                "model_detail": {
                    "name": "书生·浦语",
                    "model_type": "聊天机器人、自然语言处理助手",
                    "version": "1.3.0",
                    "base_model": "GShard-v2-xlarge",
                    "parameter_volume": "约50亿个参数",
                    "pretraining_info": "包含约7500亿个英文和中文字词的大规模无标签文本数据集",
                    "finetuning_info": "通过Fine-tuning在任务特定数据集上进行微调",
                    "alignment_info": "根据不同任务需求选择相应的数据集进行微调，如问答、摘要、机器翻译等任务",
                    "endpoint": "RLHF对齐方法",
                    "access_key": "",
                    "secret_key": "",
                },
                "record_file": ["书生·浦语 1.3.0", "送评模型1 1.0", "送评模型1 1.4"],
            },
        )


class ShowModelCard(Display):
    template = "widgets/model_card.html"

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
