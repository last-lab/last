from fastapi import APIRouter, Depends, Path, UploadFile, File
from jinja2 import TemplateNotFound
from pydantic import BaseModel
from starlette.requests import Request


from dashboard.models import DataSet
from last.services.depends import (
    create_checker,
    get_model_resource,
    get_resources,
)
from last.services.resources import Model as ModelResource
from last.services.template import templates

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
    contents = {
        "result": 1,
        "reason": "评测集已存在",
        "type": "国家安全",
        "detail": [
            {"subType": "颠覆国家政权", "thirdType": ["三级维度1", "三级维度2"]},
            {"subType": "宣传恐怖主义", "thirdType": ["三级维度3", "三级维度4"]},
        ],
        "dataCount": 666,
        "number": 10000,
        "size": "10.6GB",
    }
    return contents


class Item(BaseModel):
    name: str
    dimensions: str


@router.post("/dataset/conform")
async def conform(request: Request, item: Item):
    print(item)
    contents = {"result": 1, "reason": "成功"}
    await DataSet.create(name=item.name, dimensions=item.dimensions)
    return contents