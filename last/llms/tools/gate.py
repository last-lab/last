from tortoise import Model, fields

from dashboard.enums import EvalStatus
from aiohttp_retry import RetryClient, ExponentialRetry
from dashboard.biz_models.eval_model import ModelInfo


async def get_gate_data():
    retry_options = ExponentialRetry(attempts=1)
    retry_client = RetryClient(raise_for_status=False,
                               retry_options=retry_options)
    _url = "http://47.103.205.73:5000/api/get_api_table"
    async with retry_client.get(_url) as response:
        # 处理响应
        try:
            result = await response.json()
            await complete_result(result)
        except Exception as e:
            result = await response.text()
    await retry_client.close()

async def complete_result(result):
    # 根据 url, 去重, 取timestamp最新的元素
    unique_data = {
        item['url']: item
        for item in sorted(
            result, key=lambda x: int(x['timestamp']), reverse=True)
    }
    result = list(unique_data.values())
    # 创建模型
    new_list = [await create_model(item['name']) for item in result]


async def create_model(llm_name):
    await ModelInfo.create(
        name=llm_name,
        endpoint=llm_name,
        access_key="None",
        secret_key="None",
        model_type="聊天机器人、自然语言处理助手",
        version="未知",
        base_model="GPT3.5-Turbo",
        parameter_volume="未知",
        pretraining_info="未知",
        finetuning_info="未知",
        alignment_info="未知",
        model_org="未知",
        auth_status=True,
    )
