import pytest
from last.types.task import TaskManager
from last.types.base import create_ORM
from last.types.model import ModelDetail
from last.types.report import ReportManager

@pytest.fixture(scope="module")
def orm():
    # 配置前后端环境，orm接口等
    orm = create_ORM(conf)
    yield orm
    # 在测试完成后执行清理操作（如果需要）

def test_find_records(orm):
    # 用户点击新建评测按钮，进入界面
    # 用户点评测方案下拉框，此时查询目前已有的评测方案（task）
    tasks = TaskManager.find_records(orm, page_num=1, page_size=10, searched_by=None, filted_by=None, sorted_by=None)
    # 确保查询结果非空
    assert len(tasks) > 0

def test_new_report(orm):
    # 创建一个模拟的评测模型
    model = ModelDetail(
        name="Mock Model",
        model_type="Mock",
        version="1.0",
        base_model="Mock Base Model",
        parameter_volume="Mock Parameter Volume",
        pretraining_info="Mock Pretraining Info",
        finetuning_info="Mock Finetuning Info",
        alignment_info="Mock Alignment Info",
        API_url="Mock API URL",
        access_key="Mock Access Key",
        secret_key="Mock Secret Key",
        max_token_length=100,
        limited_token=1000,
        max_access_per_hour=100,
        max_access_per_min=10
    )

    # 系统测试模型API是否可用
    res = ReportManager.load_model_api(model)

    # 配置单次评测
    new_report = Report(
        model_name=model.name,
        version=model.version,
        display_name=f'{model.name} {model.version}',
        task_name=task.name,
        task_detail=task,  
        state=None,  
        report_detail=None, 
        model_detail=None,  
        registration=None  
    )

    # 新建评测，返回id
    report_id = ReportManager.new(orm, new_report)
    # 确保评测ID非空
    assert report_id is not None

def test_find_records_with_filter(orm):
    # 创建一个模拟的评测模型
    model = ModelDetail(
        name="Mock Model",
        model_type="Mock",
        version="1.0",
        base_model="Mock Base Model",
        parameter_volume="Mock Parameter Volume",
        pretraining_info="Mock Pretraining Info",
        finetuning_info="Mock Finetuning Info",
        alignment_info="Mock Alignment Info",
        API_url="Mock API URL",
        access_key="Mock Access Key",
        secret_key="Mock Secret Key",
        max_token_length=100,
        limited_token=1000,
        max_access_per_hour=100,
        max_access_per_min=10
    )

    # 系统测试模型API是否可用
    res = ReportManager.load_model_api(model)

    # 配置单次评测
    new_report = Report(
        model_name=model.name,
        version=model.version,
        display_name=f'{model.name} {model.version}',
        task_name=task.name,
        task_detail=task,  
        state=None,  
        report_detail=None, 
        model_detail=None,  
        registration=None  
    )

    # 新建评测，返回id
    report_id = ReportManager.new(orm, new_report)
    
    # 创建一个筛选器
    my_filter = Filter(field="model_name", operator='equal', context=new_report.model_name)

    # 寻找评测记录
    report_ids = ReportManager.find_records(orm, page_num=1, page_size=10, searched_by=None, filted_by=my_filter, sorted_by=None)
    reports = ReportManager.get_records(orm, report_ids)
    # 确保筛选后的结果非空
    assert len(reports) > 0