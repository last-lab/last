from tortoise import Tortoise

from dashboard.biz_models import LabelPage, LabelResult


async def create_labeling_mock_data():
    connection = Tortoise.get_connection("default")
    await connection.execute_query(f"DROP TABLE IF EXISTS {LabelPage.__name__.upper()}")
    await Tortoise.generate_schemas(LabelPage)
    # mock_data = LabelPage(
    #     task_id = "2023-09-14 12:00:00",
    #     labeling_method = "2023-09-14 12:00:00",
    #     dateset = "2023-09-14 12:00:00",
    #     create_time = "2023-09-14 12:00:00",
    #     current_status = "未标注"
    # )
    # await mock_data.save()

    await connection.execute_query(f"DROP TABLE IF EXISTS {LabelResult.__name__.upper()}")
    await Tortoise.generate_schemas(LabelResult)
