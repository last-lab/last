import csv
import json
import time

import pandas as pd
from starlette.requests import Request

from dashboard.biz_models import DataSet, EvaluationPlan, LabelPage, LabelResult, ModelInfo, Risk
from dashboard.enums import EvalStatus
from dashboard.models import Admin
from dashboard.utils.converter import DataSetTool
from last.services.resources import ComputeField
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

        # 判空
        if eval_plan is not None:
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

            return await super().render(
                request,
                {"plan_detail": plan_detail},
            )
        else:
            return await super().render(
                request,
                {"plan_detail": {}},
            )


class OperationField(ComputeField):
    def __init__(self, **context):
        super().__init__(**context)
        self.display = ShowOperation(**context)

    async def get_value(self, request: Request, obj: dict):
        return {
            "id": obj["id"],
            "llm_id": obj["llm_id"],
            "report": obj["report"],
        }


class ShowOperation(Display):
    template = "record/record_operations.html"

    def __init__(self, **context):
        super().__init__(**context)

    async def render(self, request: Request, value: any):
        model_ids = []
        llm_ids = value["llm_id"].split(",")
        for i in llm_ids:
            info = await ModelInfo.get_or_none(id=int(i)).values()
            model_ids.append({"id": i, "name": info["name"], "model_detail": info})

        # TODO: 下面的 record(备案文件) 需要替换为查询得到文件列表
        record_file = []
        record = ["chatgpt"]
        # 找到对应的pdf
        for item in record:
            record_file.append({"name": item, "url": "/static/reg/" + item + ".pdf"})

        return await super().render(
            request,
            {
                "id": value["id"],
                "model_ids": model_ids,
                "record_file": record_file,
                "report": value["report"],
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
        content = {}
        label_info = []
        if value is not None:
            dataset = await DataSet.get_or_none(uid=value).values()
            risk = json.loads(dataset["focused_risks"])
            for i in risk:
                res = await Risk.get_or_none(risk_id=i).values()
                if res is not None:
                    if res["risk_level"] == 1:
                        content = {
                            "risk_level": res["risk_level"],
                            "risk_id": res["risk_id"],
                            "risk_name": res["risk_name"],
                            "risk_description": res["risk_description"],
                            "child_risk": [],
                        }
                    elif res["risk_level"] == 2:
                        content["child_risk"].append(
                            {
                                "risk_level": res["risk_level"],
                                "risk_id": res["risk_id"],
                                "risk_name": res["risk_name"],
                                "risk_description": res["risk_description"],
                                "third_risk": [],
                            }
                        )
                    elif res["risk_level"] == 3:
                        filter_info = list(
                            filter(
                                lambda item: item["risk_id"] == res["parent_risk_id"],
                                content["child_risk"],
                            )
                        )
                        if len(filter_info) > 0:
                            filter_info[0]["third_risk"].append(
                                {
                                    "risk_id": res["risk_id"],
                                    "risk_name": res["risk_name"],
                                    "risk_description": res["risk_description"],
                                }
                            )
            if dataset["file"].endswith("csv"):
                with open(dataset["file"], "r", encoding="utf-8-sig") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        info = row
                        label_info.append(info)
                del label_info[0]
            elif dataset["file"].endswith("xlsx"):
                xls = pd.ExcelFile(dataset["file"])
                for sheet_name in xls.sheet_names:
                    # Read the sheet into a DataFrame
                    df = pd.read_excel(xls, sheet_name=sheet_name)
                    for index, row in df.iterrows():
                        label_info.append(list(row))
            else:
                raise NotImplementedError("We only support csv or xlsx file.")

        value = await super().render(
            request, {**dataset, "focused_risks": content, "label_info": label_info}
        )
        return value


class ShowRiskType(Display):
    template = "dataset/risk.html"

    async def render(self, request: Request, value: any):
        label = ""
        for i in json.loads(value):
            res = await Risk.get_or_none(risk_id=i).values()
            if res is not None:
                if res["risk_level"] == 1:
                    label = res["risk_name"]
        return await super().render(request, {"content": label})


class ShowSecondType(Popover):
    # template = "dataset/risk_second.html"

    async def render(self, request: Request, value: any):
        label = []
        for i in json.loads(value):
            res = await Risk.get_or_none(risk_id=i).values()
            if res is not None:
                if res["risk_level"] == 2:
                    label.append(res["risk_name"])
        return await super().render(
            request,
            {"content": ",".join([d for d in label]), "popover": ",".join([d for d in label])},
        )


class RiskAction(Display):
    template = "risk/risk_action.html"

    async def render(self, request: Request, value: any):
        risk_info = await Risk.get_or_none(risk_id=value).values()
        return await super().render(request, {**risk_info})


class ShowRisk(Display):
    template = "risk/risk_show.html"

    async def render(self, request: Request, value: any):
        name = ""
        content = await Risk.get_or_none(risk_id=value).values()
        if content["risk_level"] == 1:
            name = content["risk_name"]
        if content["risk_level"] == 2:
            res = await Risk.get_or_none(risk_id=content["parent_risk_id"]).values()
            name = res["risk_name"]
        return await super().render(
            request,
            {"content": name},
        )


class ShowSecondRisk(Display):
    template = "risk/risk_show.html"

    async def render(self, request: Request, value: any):
        name = ""
        content = await Risk.get_or_none(risk_id=value).values()
        if content["risk_level"] == 2:
            name = content["risk_name"]
        return await super().render(
            request,
            {"content": name},
        )


class ShowSecondRiskDesc(Display):
    template = "risk/risk_second_desc_show.html"

    async def render(self, request: Request, value: any):
        description = ""
        content = await Risk.get_or_none(risk_id=value).values()
        if content["risk_level"] == 2:
            description = content["risk_description"]
        return await super().render(
            request,
            {"content": description},
        )


class ShowPlan(Display):
    template = "evaluationplan/update_plan.html"

    async def render(self, request: Request, value: any):
        info = await EvaluationPlan.get_or_none(name=value).values()
        return await super().render(
            request,
            {"content": info["id"], "name": value, "id": info["id"]},
        )


class ShowLabel(Display):
    template = "labelpage/label_detail.html"

    async def render(self, request: Request, value: any):
        info = await LabelPage.get_or_none(task_id=value).values()
        return await super().render(
            request,
            {"content": info["id"]},
        )


class ShowLabelProgress(Display):
    template = "labelpage/progress_show.html"

    async def render(self, request: Request, value: any):
        user_id = str(request.state.admin).split("#")[1]
        info = await LabelPage.get_or_none(task_id=value).values()
        assign_length_dict = eval(info["assign_length"])
        assign_labeling_progress = eval(info["labeling_progress"])
        # 已经标注了的题目数量
        labeled_question_count = assign_labeling_progress[user_id]
        total_question_count = assign_length_dict[user_id]
        # return content
        if labeled_question_count == total_question_count:
            return_content = "已完成"
        else:
            return_content = f"标注中 \n {labeled_question_count}/{total_question_count}"

        return await super().render(request, {"content": return_content})


class ShowTaskLabelingProgress(Display):
    template = "taskmanage/labeling_progress_show.html"

    async def render(self, request: Request, value: any):
        info_list = await LabelResult.filter(task_id=value)
        total_question = len(info_list)
        labeled_count = 0
        for info in info_list:
            if info.status == "标注完成":
                labeled_count += 1

        if labeled_count == total_question:
            return_content = "已完成"
        else:
            return_content = f"标注中 \n {labeled_count}/{total_question}"
        return await super().render(request, {"content": return_content})


class ShowTaskAuditProgress(Display):
    template = "taskmanage/audit_progress_show.html"

    async def render(self, request: Request, value: any):
        user_id = str(request.state.admin).split("#")[1]
        return user_id


class ShowTime(Display):
    template = "record/time_format.html"

    async def render(self, request: Request, value: int):
        time_array = time.localtime(value / 1000)
        format_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        return await super().render(
            request,
            {"content": format_time},
        )


class ShowAdmin(Display):
    template = "admin/admin_action.html"

    async def render(self, request: Request, value: any):
        info = await Admin.get_or_none(username=value).values()
        return await super().render(
            request,
            {"content": info["id"], "name": value, "id": info["id"]},
        )
