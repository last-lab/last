# 清楚AuditPage和AuditResult两张表
from tortoise import Tortoise

from dashboard.biz_models import AuditPage, AuditResult


async def create_audit_mock_data():
    connection = Tortoise.get_connection("default")
    await connection.execute_query(f"DROP TABLE IF EXISTS {AuditPage.__name__.upper()}")
    await Tortoise.generate_schemas(AuditPage)
    # mock_data = LabelPage(
    #     task_id = "2023-09-14 12:00:00",
    #     labeling_method = "2023-09-14 12:00:00",
    #     dateset = "2023-09-14 12:00:00",
    #     create_time = "2023-09-14 12:00:00",
    #     current_status = "未标注"
    # )
    # await mock_data.save()

    await connection.execute_query(f"DROP TABLE IF EXISTS {AuditResult.__name__.upper()}")
    await Tortoise.generate_schemas(AuditResult)
