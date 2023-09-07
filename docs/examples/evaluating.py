from last.types.task import TaskManager
from last.types.base import create_ORM
from last.types.model import ModelDetail
from last.types.report import ReportManager



with last.Client(server_address="http://localhost:5000") as client:# TODO: BaseClient

    dataset = Dataset(uid="uuid4")
    model = Model(endpoint="xxx", key='xxx') # Init:test, exception
    task = Task(dataset, model, creator='xxx')

    report:Report, results: Dataset = task.run(return_detail=true) # if return_detail, return all response

    results.ready() # TODO: add async

    report.render(file_path='xxx', type='pdf')

    new_data = annote(results)

    new_data.save()

# _Context
# context = None, context = get_current_context(), contextlib


# 用户点击新建评测按钮，进入界面
# 用户点评测方案下拉框，此时查询目前已有的评测方案（task）
tasks = TaskManager.find_records(orm, page_num=1, page_size=10, searched_by=None, filted_by=None, sorted_by=None)

# 用户选择一个task
task = tasks[0]

# 用户添加一个评测模型
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


my_filter = Filter(field = "model_name",
    operator = 'equal',
    context=new_report.model_name)
    
# 寻找评测记录
report_ids = ReportManager.find_records(orm, page_num=1, page_size=10, searched_by=None, filted_by=my_filter, sorted_by=None)
reports = ReportManager.get_records(orm, report_ids)
