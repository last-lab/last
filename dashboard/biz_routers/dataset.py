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


# 上传数据集页面的路由
@router.get("/{resource}/upload_dataset", dependencies=[Depends(create_checker)])
async def upload_dataset(
    request: Request,
    resource: str = Path(...),
    resources=Depends(get_resources),
    model_resource: ModelResource = Depends(get_model_resource),
):
    risk_info = await Risk.all().filter(risk_level=1)
    for first_risk in risk_info:
        second_risks = await Risk.all().filter(risk_level=2, parent_risk_id=first_risk.risk_id)
        first_risk.second_risks = second_risks
        for second_risk in second_risks:
            third_risks = await Risk.all().filter(risk_level=3, parent_risk_id=second_risk.risk_id)
            second_risk.third_risks = third_risks
    context = {
        "request": request,
        "resource": resource,
        "resource_label": model_resource.label,
        "resources": resources,
        "model_resource": model_resource,
        "page_title": "上传数据集",
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


# 上传解析操作
@router.post("/dataset/json")
async def json(request: Request, file: UploadFile = File(...)):
    await upload.upload(file)
    contents = Dataset(file=os.path.join(BASE_DIR, "static", "uploads", file.filename))
    return contents


class Item(Dataset):
    focused_risks: str
    focused_risks_json: str
    first_risk_id: str


# 提交操作
@router.post("/dataset/conform")
async def conform(request: Request, item: Item):
    result = await DataSet.all().filter(name=item.name)
    if len(result) > 0:
        return {"result": 0, "reason": "数据集名称重复，请修改"}
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
            first_risk_id=item.first_risk_id,
        )
        return {"result": 1, "reason": "上传成功"}
