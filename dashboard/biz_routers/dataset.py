import os

from fastapi import APIRouter, Depends, File, Path, UploadFile
from jinja2 import TemplateNotFound
from starlette.requests import Request

from dashboard.biz_models import DataSet
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
    # TODO 风险类型需调用接口获取，此处先mock
    risk_info = [
        {
            "id": "risk1",
            "level": 2,
            "name": "颠覆国家政权",
            "downlevel_risk_name": [
                {
                    "id": "risk1-1",
                    "name": "反政府组织",
                },
                {
                    "id": "risk1-2",
                    "name": "暴力政治活动",
                },
                {
                    "id": "risk1-3",
                    "name": "革命行动",
                },
            ],
        },
        {
            "id": "risk2",
            "level": 2,
            "name": "宣扬恐怖主义",
            "downlevel_risk_name": [
                {
                    "id": "risk2-1",
                    "name": "恐怖组织宣传",
                },
                {
                    "id": "risk2-2",
                    "name": "暴力恐吓手段",
                },
                {
                    "id": "risk2-3",
                    "name": "恐怖袭击策划",
                },
            ],
        },
        {
            "id": "risk3",
            "level": 2,
            "name": "挑拨民族对立",
            "downlevel_risk_name": [
                {
                    "id": "risk3-1",
                    "name": "种族仇恨煽动",
                },
                {
                    "id": "risk3-2",
                    "name": "民族主义煽动",
                },
                {
                    "id": "risk3-3",
                    "name": "社会分裂策略",
                },
            ],
        },
    ]
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
