import asyncio
import unittest

from last.client.call_llm import generate


async def generation_test(prompt, model):
    system_prompt = None
    maximum_length = 256
    temperature = 0.00001
    stop_sequence = None
    top_p = 0.9
    frequence_penalty = 0.0
    presence_penalty = 0.0

    generated_text = await generate(
        prompt,
        model,
        system_prompt,
        maximum_length,
        temperature,
        stop_sequence,
        top_p,
        frequence_penalty,
        presence_penalty,
    )

    return generated_text

# todo 1 从数据库中读取现有的llm info
# todo 2 根据llm name 用 generated_text = asyncio.run(generation_test(prompt="中国的首都在哪里", model="tigerbot")) 的方式调用模型
# todo 3 异常捕获
# todo 4 根据访问结果重写数据库
        

import asyncio
import sched
import time
from tortoise import Tortoise, fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import DoesNotExist

from dashboard.biz_models import (
    AuditPage,
    AuditResult,
    DataSet,
    EvaluationPlan,
    LabelPage,
    LabelResult,
    ModelInfo,
    Risk,
)
from dashboard.enums import EvalStatus
from dashboard.models import Admin
from dashboard.utils.converter import DataSetTool
from last.services.resources import ComputeField
from last.services.widgets.displays import Display, Popover, Status

# 创建一个全局的调度器对象
scheduler = sched.scheduler(time.time, time.sleep)

async def task():
    ...

async def check_model_api_alives():
    """检查当前数据库中存储的model提供的api是否可用
    """
    model_infos = await ModelInfo.all()
    for llm_info in model_infos:
        llm_name = llm_info.name
        generated_text = await generation_test(prompt="hello", model=llm_name)
        if generated_text.startswith("error:"):
            print("********************************")
            print("False")
            print(llm_name)
            print(generated_text)
            llm_info.auth_status = False
        else:
            print("********************************")
            print("True")
            print(llm_name)
            print(generated_text)
            llm_info.auth_status = True
        # 将更新后的 llm_info 保存回数据库
        await llm_info.save()
        