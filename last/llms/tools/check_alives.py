import asyncio
import schedule

from last.client.call_llm import generate
        
import asyncio
import time
from dashboard.biz_models import (
    ModelInfo,
)
import threading

# 每隔 8mins 测试一轮 API
inc = 60 * 8

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

async def check_model_api_alives():
    """检查当前数据库中存储的model提供的api是否可用
    """
    model_infos = await ModelInfo.all()
    for llm_info in model_infos:
        llm_name = llm_info.name
        # 访问 API
        generated_text = await generation_test(prompt="你好,我现在有一些问题需要咨询你,请问你可以帮忙回答一下么", model=llm_name)
        if generated_text.startswith("error:"):
            # error 在 generate 内部消化，以前缀获取是否返回 error
            llm_info.auth_status = False
        else:
            llm_info.auth_status = True
        # 将更新后的 llm_info 保存回数据库
        await llm_info.save()
    
def run_coroutine():
    """将 check_model_api_alives 包装成同步函数, 供线程直接调用
    """    
    asyncio.run(check_model_api_alives())
    
def run_schedule():
    """调度器线程执行函数
    每 inc + 1 秒检查一下是否需要执行任务
    """ 
    # 立即检查一次API
    asyncio.run(check_model_api_alives())
    while True:
        schedule.run_pending()
        # 每 inc 秒新增一个任务，则每 inc + 1 秒唤醒 schedule 线程查看并执行任务
        time.sleep(inc + 1)
        
async def run_check_model_api_alives():
    """检查各模型 API 是否可用, 结果写入DB
    """    
    # 定时任务, 每 inc 秒执行一次
    schedule.every(inc).seconds.do(run_coroutine)
    # 负责定期检查并启动 schedule 中任务的线程
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()
