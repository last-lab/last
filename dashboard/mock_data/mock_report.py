from tortoise import Tortoise

from dashboard.biz_models.eval_model import ModelResult


async def create_mock_report():
    connection = Tortoise.get_connection("default")
    await connection.execute_query(f"DROP TABLE IF EXISTS {ModelResult.__name__.upper()}")
    await Tortoise.generate_schemas(ModelResult)

    await ModelResult(record_id=1, eval_model_id=1, eval_type_id=0, score=88).save()
    await ModelResult(record_id=1, eval_model_id=2, eval_type_id=0, score=68).save()

    await ModelResult(
        record_id=1,
        eval_model_id=1,
        eval_type_id=1,
        score=90,
        eval_data_set_score_json='[{"id":"1","score":"75"}]',
    ).save()
    await ModelResult(
        record_id=1,
        eval_model_id=2,
        eval_type_id=1,
        score=77,
        eval_data_set_score_json='[{"id":"1","score":"78"}]',
    ).save()

    await ModelResult(
        record_id=1,
        eval_model_id=1,
        eval_type_id=2,
        score=97,
        eval_data_set_score_json='[{"id":"2","score":"88"}]',
    ).save()

    await ModelResult(
        record_id=1,
        eval_model_id=2,
        eval_type_id=2,
        score=85,
        eval_data_set_score_json='[{"id":"2","score":"88"}]',
    ).save()
