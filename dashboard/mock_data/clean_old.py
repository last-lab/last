from tortoise import Tortoise

from dashboard.biz_models import Record
from dashboard.enums import EvalStatus


async def clean_old_record():
    Tortoise.get_connection("default")
    # await connection.execute_query(f"DROP TABLE IF EXISTS {Record.__name__.upper()}")
    await Tortoise.generate_schemas(Record)

    await Record.filter(state=EvalStatus.on_progress).delete()
