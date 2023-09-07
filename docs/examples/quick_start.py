""" For TY & YC
load types and client

clients'admin served at services.

"""

from last.types.task import TaskManager, TaskInfo
from last.types.base import create_ORM
from last.types.model import APIModelInfo, APIModelManager
from last.types.report import ReportManager
from last.types.dataset import DatasetInfo, DatasetManager


with last.Client(server_address="http://localhost:5000") as client:# TODO: BaseClient
    dataset_info = DatasetInfo(name="xxx", dimensions="国家安全", url='http://xxxxxx')
    # 如果需要加载新数据集, 则提供DatasetInfo，内含数据集访问链接，返回dataset uid="uuid4"
    dataset_id = DatasetManager.new(dataset_info) 
    # 明确评测方案，即使用哪些数据集进行评测
    task = TaskInfo(name="xxx", datasets=[dataset_id])

    # 配置评测模型API TODO 初始化test 异常捕捉 
    model = APIModelInfo(API_url="xxx", access_key='xxx', secret_key='xxx') 

    # 执行一次评测任务, 返回任务id
    report_id = ReportManager.new(task, model)  
    # 拉取评测结果 
    report, QAs = ReportManager.get_records([report_id], verbose=True)  # if return_detail, return all response
    # 保存评测报告到本地
    report.render(file_path='xxx', type='pdf') 
    # 上传评测QA历史到数据库
    new_dataset_id = DatasetManager.upload(QAs)
    # 对新的dataset创建一个标注任务
    annotation_id = AnnotationManager.new(new_dataset_id) 
