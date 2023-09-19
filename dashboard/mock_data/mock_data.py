from .mock_labeling_data import create_labeling_mock_data
from .mock_dataset import create_mock_dataset

async def create_mock_data():
    await create_labeling_mock_data()
    await create_mock_dataset()
