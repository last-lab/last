from .mock_labeling_data import create_labeling_mock_data
from .mock_report import create_mock_report
from .mock_risk import create_mock_risk
from .mock_task import create_task


async def create_mock_data():
    await create_labeling_mock_data()
    # await create_mock_dataset()
    await create_task()
    await create_mock_risk()
    await create_mock_report()
