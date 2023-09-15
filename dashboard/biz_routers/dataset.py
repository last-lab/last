from fastapi import APIRouter, Depends, File, Path, UploadFile
from jinja2 import TemplateNotFound
from pydantic import BaseModel
from starlette.requests import Request

from dashboard.biz_models import DataSet
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
    context = {
        "request": request,
        "resource": resource,
        "resource_label": model_resource.label,
        "resources": resources,
        "model_resource": model_resource,
        "page_title": "上传评测集",
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
    # contents = await upload.upload(file)
    contents = {
        "result": 1,
        "reason": "",
        "focused_risks": [
            {"level":1,"name":"国家安全","description":""},
            {
                "level":2,
                "name":"颠覆政权",
                "description":"",
                "uplevel_risk_name": ["敏感信息", "安全问题"]
            },
            {
                "level": 2,
                "name": "宣扬恐怖主义",
                "description": "",
                "uplevel_risk_name": ["维度三1", "维度三2"]
            },
        ],
        "qa_num": 666,
        "word_cnt": 1000,
        "volume": "10GB"
    }
    return contents


class Item(BaseModel):
    name: str
    focused_risks: str
    volume: str
    qa_num: str
    word_cnt: str

@router.post("/dataset/conform")
async def conform(request: Request, item: Item):
    result = await DataSet.all().filter(name=item.name)
    if len(result) > 0:
        return {"result": 0, "reason": "评测集名称重复，请修改"}
    else:
        await DataSet.create(
            name=item.name,
            focused_risks=item.focused_risks,
            volume=item.volume,
            qa_num=item.qa_num,
            word_cnt=item.word_cnt,
        )
        return {"result": 1, "reason": "上传成功"}
