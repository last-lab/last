from typing import Type

from fastapi import APIRouter, Depends, Path
from jinja2 import TemplateNotFound
from starlette.requests import Request
from tortoise import Model
from dashboard.biz_models.task_manage_model import TaskManage
from last.services.depends import get_model, get_model_resource, get_resources
from last.services.depends import create_checker
from last.services.resources import Model as ModelResource
from last.services.template import templates
from last.services.routes.resources import list_view
router = APIRouter()

@router.get("/{resource}/labeling/{pk}")
async def labeling_view(
    request: Request,
    resource: str = Path(...),
    pk: str = Path(...),
    model_resource: ModelResource = Depends(get_model_resource),
    resources=Depends(get_resources),
    model: Type[Model] = Depends(get_model),
):

    context = {
        "request": request,
        "resources": resources,
        "resource_label": model_resource.label,
        "resource": resource,
        "pk": 1,
        "model_resource": model_resource,
        "page_title": model_resource.page_title,
        "page_pre_title": model_resource.page_pre_title,
    }
    # 点击了标注之后，需要根据传回来的参数，主要是数据集的名称，标注方式
    # 载入数据，丢一个新的界面出去

    try:
        return templates.TemplateResponse(
            f"{resource}/label.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "label.html",
            context=context,
        )



@router.get("/{resource}/display/{pk}")
async def labeling_view(
    request: Request,
    resource: str = Path(...),
    pk: str = Path(...),
    model_resource: ModelResource = Depends(get_model_resource),
    resources=Depends(get_resources),
    model: Type[Model] = Depends(get_model),
):
    obj = await model.get(pk=pk).prefetch_related(*model_resource.get_m2m_field())
    # 获取得到对应task的id
    task_id = obj.task_id
    # 从task表中获取得到指定task_id的那一条记录
    task = await TaskManage.get(task_id=task_id)
    # 获取数据集的名字，获取文件的路径，读取文件，返回所有的问题
    dataset_name = getattr(task, "dateset")
    # 根据这个数据集的名字，

    context = {
        "request": request,
        "resources": resources,
        "resource_label": model_resource.label,
        "resource": resource,
        "pk": pk,
        "model_resource": model_resource,
        "page_title": model_resource.page_title,
        "page_pre_title": model_resource.page_pre_title,
    }
    try:
        return templates.TemplateResponse(
            f"{resource}/brief_dataset.html",
            context=context,
        )
    except TemplateNotFound:
        return templates.TemplateResponse(
            "brief_dataset.html",
            context=context,
        )


@router.get("/{resource}/get_dataset_brief_data")
async def get_dataset_brief_from_db(request: Request, resource: str):
    # 需要有task id的名字，然后根据这个名字从task table中获取得到对应的dataset的名字
    # 再从dataset表中取出来dataset的文件路径
    # 读取这个文件的路径获取得到文件的数据

    return [
        {
            "id": 1,
            "question": "问题1",
            "status": "标注中",
            "action": "标注"
        },
        {
            "id": 2,
            "question": "问题2",
            "status": "已完成",
            "action": "查看"
        },
        {
            "id": 3,
            "question": "问题3",
            "status": "标注中",
            "action": "标注"
        }
    ]



@router.post("/{resource}/labeling/get_config")
async def get_config_from_db(request: Request, resource: str):
    """_summary_
    # 需要返回 id，支持数据库的搜索

    Args:
        request (Request): _description_
        resource (str): _description_
    """
    # TODO, 根据request中的参数查找数据库，生成如下形式的数据返回给前端
    mock_data = {
        "tags": [
            {"value": "Person", "background": "red"},
            {"value": "Organization", "background": "darkorange"},
        ],
        "text": "这是一段测试文本",
    }
    # return "test"
    return mock_data


@router.post("/{resource}/labeling/get_data")
async def get_annotatoin_and_predict_data(request: Request, resource: str):
    """_summary_
    # 需要返回labelstudio需要的annotation和predict的两个数据

    Args:
        request (Request): _description_
        resource (str): _description_
    """
    mock_data = {"annotations": [], "predictions": []}
    return mock_data


@router.post("/{resource}/labeling/{pk}/submit")
async def submit_callback(request: Request, resource: str, pk: str):
    form = await request.form()
    print(form)
