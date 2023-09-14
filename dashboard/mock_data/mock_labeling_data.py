from tortoise import Tortoise

from dashboard.models import LabelPage


async def create_labeling_mock_data():
    connection = Tortoise.get_connection("default")
    await connection.execute_query(f"DROP TABLE IF EXISTS {LabelPage.__name__.upper()}")
    await Tortoise.generate_schemas(LabelPage)
    label_page_1 = LabelPage(
        task_type="Type 1",
        labeling_method="Method 1",
        release_time="2023-09-14 12:00:00",
        current_status="Pending",
    )
    await label_page_1.save()

    label_page_2 = LabelPage(
        task_type="Type 2",
        labeling_method="Method 2",
        release_time="2023-09-15 09:30:00",
        current_status="InProgress",
    )
    await label_page_2.save()

    label_page_3 = LabelPage(
        task_type="Type 3",
        labeling_method="Method 3",
        release_time="2023-09-16 15:45:00",
        current_status="Completed",
    )
    await label_page_3.save()
