# 标注相关重新初始化
# 数据相关重新初始化
from .clean_old import clean_old_record

# 系统必须的初始化
from .mock_llms import create_mock_llms
from .mock_risk import create_mock_risk

# from .mock_audit_data import create_audit_mock_data
# from .mock_labeling_data import create_labeling_mock_data

# from .mock_task import create_task

# from .mock_dataset import create_mock_dataset


# 评测报告重新初始化
# from .mock_report import create_mock_report
# from .mock_risk_demo import create_mock_risk_demo


async def create_mock_data():
    # await create_labeling_mock_data()
    # await create_task()
    # await create_audit_mock_data()

    await create_mock_risk()
    await create_mock_llms()

    # await create_mock_report()
    # await create_mock_risk_demo()

    # await create_mock_dataset()
    await clean_old_record()
