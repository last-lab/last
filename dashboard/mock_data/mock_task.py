from tortoise import Tortoise
from uuid import uuid4
from datetime import datetime
from dashboard.biz_models import TaskManage


async def create_task():
    connection = Tortoise.get_connection("default")
    await connection.execute_query(f"DROP TABLE IF EXISTS {TaskManage.__name__.upper()}")
    await Tortoise.generate_schemas(TaskManage)
    # mockdata =  TaskManage(
    #     task_id = "2023-09-14 12:00:00",
    #     labeling_method = "2023-09-14 12:00:00",
    #     dateset = "2023-09-14 12:00:00",
    #     create_time = "2023-09-14 12:00:00",
    #     current_status = "未标注"
    # )
    # await mockdata.save()
    # fields_dict = TaskManage._meta.fields_map
    # for field_name, field in fields_dict.items():
    #     print(f"Field: {field_name}, Type: {field.__class__.__name__}")
