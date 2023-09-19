from dashboard.biz_models import DataSet
from tortoise import Tortoise

async def create_mock_dataset():
    connection = Tortoise.get_connection("default")
    await connection.execute_query(f"DROP TABLE IF EXISTS {DataSet.__name__.upper()}")
    await Tortoise.generate_schemas(DataSet)

    dataset_1 = DataSet(
        name = "test_set_1",
        focused_risks = "[]",
        url = "null",
        file = "null",
        volume = "20GB",
        used_by = 0,
        qa_num = 15,
        word_cnt = 15000,
        qa_records = "",
        conversation_start_id = '0',
        current_conversation_index = 0,
        current_qa_record_id = 0
    )
    await dataset_1.save()


    dataset_2 = DataSet(
        name = "test_set_2",
        focused_risks = "[]",
        url = "null",
        file = "null",
        volume = "20GB",
        used_by = 0,
        qa_num = 20,
        word_cnt = 20000,
        qa_records= "",
        conversation_start_id = "0",
        current_conversation_index = 0,
        current_qa_record_id = 0
    )

    await dataset_2.save()
