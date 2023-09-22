from tortoise import Tortoise

from dashboard.biz_models import DataSet


async def create_mock_dataset():
    connection = Tortoise.get_connection("default")
    await connection.execute_query(f"DROP TABLE IF EXISTS {DataSet.__name__.upper()}")
    await Tortoise.generate_schemas(DataSet)

    # dataset_1 = DataSet(
    #     name="Product ABC",
    #     focused_risks="[]",
    #     url="https://example.com",
    #     file="document.pdf",
    #     volume="10 GB",
    #     used_by=100,
    #     qa_num=5,
    #     word_cnt=500,
    #     updated_at="2021-09-19 15:30:00",
    #     qa_records="Record 1: Lorem ipsum...",
    #     conversation_start_id="abc123",
    #     current_conversation_index=1,
    #     current_qa_record_id=1,
    #     uid="user123",
    #     description="This is a sample dataset",
    #     creator="John Doe",
    #     editor="Jane Smith",
    #     reviewer="Alice Johnson",
    #     created_at="2021-09-19 10:00:00",
    #     permissions="read-write",
    # )
    #
    # await dataset_1.save()
    #
    # dataset_2 = DataSet(
    #     name="Service XYZ",
    #     focused_risks="[]",
    #     url="http://localhost:8000",
    #     file="image.jpg",
    #     volume="500 MB",
    #     used_by=50,
    #     qa_num=10,
    #     word_cnt=1000,
    #     updated_at="2021-09-20 09:45:00",
    #     qa_records="Record 1: Dolor sit amet...",
    #     conversation_start_id="xyz789",
    #     current_conversation_index=2,
    #     current_qa_record_id=2,
    #     uid="admin456",
    #     description="This is another sample dataset",
    #     creator="Alice Smith",
    #     editor="Bob Johnson",
    #     reviewer="John Doe",
    #     created_at="2021-09-20 08:30:00",
    #     permissions="read-only",
    # )
    # await dataset_2.save()
