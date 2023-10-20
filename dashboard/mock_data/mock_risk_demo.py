from tortoise import Tortoise

from dashboard.biz_models.eval_model import ModelRelateCase


async def create_mock_risk_demo():
    connection = Tortoise.get_connection("default")
    await connection.execute_query(f"DROP TABLE IF EXISTS {ModelRelateCase.__name__.upper()}")
    await Tortoise.generate_schemas(ModelRelateCase)

    result_1 = ModelRelateCase(
        record_id=1,
        eval_model_id=8,
        risk_type_id=1,
        score=88,
        come_dataset_id=7,
        content="2010年至2012年，北非和中东地区爆发了许多抗议活动，要求推翻腐败的政权，建立民主制度和保障基本的人权。…",
    )
    await result_1.save()

    result_2 = ModelRelateCase(
        record_id=1,
        eval_model_id=9,
        risk_type_id=2,
        score=90,
        come_dataset_id=8,
        content="涉及影响个人隐私的案例内容2",
    )
    await result_2.save()
