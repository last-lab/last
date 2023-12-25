from tortoise import Tortoise

from dashboard.biz_models import Risk


async def create_mock_risk():
    connection = Tortoise.get_connection("default")
    await connection.execute_query(f"DROP TABLE IF EXISTS {Risk.__name__.upper()}")
    await Tortoise.generate_schemas(Risk)

    await Risk(risk_level=1, risk_id="0", risk_name="多样测试题").save()
    await Risk(risk_level=1, risk_id="1", risk_name="违反社会主义核心价值观").save()
    await Risk(risk_level=1, risk_id="2", risk_name="歧视相关").save()
    await Risk(risk_level=1, risk_id="3", risk_name="商业违法违规").save()
    await Risk(risk_level=1, risk_id="4", risk_name="侵害他人合法权益").save()
    await Risk(risk_level=1, risk_id="5", risk_name="无法满足特定服务类型的安全需求").save()
    await Risk(risk_level=1, risk_id="6", risk_name="模型应拒答的问题").save()
    await Risk(risk_level=1, risk_id="7", risk_name="不应该拒答问题").save()