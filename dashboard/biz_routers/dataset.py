import json as jsonp
import os

from fastapi import APIRouter, Depends, File, Path, UploadFile
from jinja2 import TemplateNotFound
from starlette.requests import Request

from dashboard.biz_models import DataSet, Risk
from dashboard.constants import BASE_DIR
from dashboard.resources import upload
from last.services.depends import create_checker, get_model_resource, get_resources
from last.services.resources import Model as ModelResource
from last.services.template import templates
from last.types.dataset import Dataset

router = APIRouter()


@router.get("/{resource}/upload_dataset", dependencies=[Depends(create_checker)])
async def upload_dataset(
    request: Request,
    resource: str = Path(...),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
):
    risk_info = []
    risks = await Risk.all()
    for risk in risks:
        if risk.risk_level == 1:
            risk_info.append(
                {
                    "risk_level": risk.risk_level,
                    "risk_id": risk.risk_id,
                    "risk_name": risk.risk_name,
                    "risk_description": risk.risk_description,
                    "child_risk": [],
                }
            )
        elif risk.risk_level == 2:
            filter_info = list(
                filter(lambda item: item["risk_id"] == risk.parent_risk_id, risk_info)
            )
            filter_info[0]["child_risk"].append(
                {
                    "risk_level": risk.risk_level,
                    "risk_id": risk.risk_id,
                    "risk_name": risk.risk_name,
                    "risk_description": risk.risk_description,
                    "third_risk": jsonp.loads(risk.third_risk) if risk.third_risk else [],
                }
            )
    context = {
        "request": request,
        "resource": resource,
        "resource_label": model_resource.label,
        "resources": resources,
        "model_resource": model_resource,
        "page_title": "上传评测集",
        "risk_info": risk_info,
    }
    try:
        return templates.TemplateResponse(
            f"{resource}/upload_dataset.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "upload_dataset.html",
            context=context,
        )


@router.post("/dataset/json")
async def json(request: Request, file: UploadFile = File(...)):
    await upload.upload(file)
    contents = Dataset(file=os.path.join(BASE_DIR, "static", "uploads", file.filename))
    return contents


class Item(Dataset):
    focused_risks: str
    focused_risks_json: str


@router.post("/dataset/conform")
async def conform(request: Request, item: Item):
    result = await DataSet.all().filter(name=item.name)
    if len(result) > 0:
        return {"result": 0, "reason": "评测集名称重复，请修改"}
    else:
        time = (
            item.created_at.year
            + "-"
            + item.created_at.month
            + "-"
            + item.created_at.day
            + " "
            + item.created_at.hour
            + ":"
            + item.created_at.minute
        )
        await DataSet.create(
            name=item.name,
            focused_risks=item.focused_risks_json,
            volume=item.volume,
            qa_num=item.qa_num,
            word_cnt=item.word_cnt,
            url=item.url,
            file=item.file,
            used_by=item.used_by,
            qa_records=str(item.qa_records),
            conversation_start_id=str(item.conversation_start_id),
            current_conversation_index=item.current_conversation_index,
            current_qa_record_id=item.current_qa_record_id,
            uid=item.uid,
            description=item.description,
            creator=str(item.creator),
            editor=item.editor,
            reviewer=item.reviewer,
            created_at=time,
            updated_at=time,
            permissions=item.permissions,
        )
        return {"result": 1, "reason": "上传成功"}
