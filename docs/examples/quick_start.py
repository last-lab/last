""" For TY & YC
load types and client

clients'admin served at services.

"""

from last.types.task import TaskManager, TaskInfo
from last.types.base import create_ORM
from last.types.model import ModelInfo
from last.types.report import ReportManager
from last.types.dataset import DatasetInfo, DatasetManager


with last.Client(server_address="http://localhost:5000") as client:# TODO: BaseClient
    # Case1 需要上传数据集, 则提供DatasetInfo，返回dataset uid="uuid4"
    dataset_id = DatasetManager.new(DatasetInfo) 
    # 明确评测方案，即使用哪些数据集进行评测，关心哪些风险维度，各个维度的评分占比
    task = TaskManager.new(TaskInfo) 
    # 配置评测模型API TODO 初始化test 异常捕捉 
    model = Model(API_url="xxx", access_key='xxx', secret_key='xxx') 
    # 执行一次评测任务
    report_id = ReportManager.new(task, model)  
    # 拉取评测结果 TODO: add async
    report, QAs = ReportManager.get_records([report_id], verbose=True)  # if return_detail, return all response
    # 保存评测报告到本地
    report.render(file_path='xxx', type='pdf') 
    # 保存评测QA历史到数据库
    new_data = DatasetManager.new(QAs)

    DatasetManager.new(new_data) # TODO: add async





# from last.types import EvaluatedContext

# # 采集->标注->训练->自测->采集 完成循环
# raw_data = load_evaluationset("set_name/uuid", "services_address") #TODO: services启动，注册数据集
# results = Report(raw_data) # 评测结果
# # TODO：progress上报
# for dim, question in raw_data:
#     answer = model.infer(toxic_question) # 模型API推理
#     results.add(dim, question, answer) # 评测结果
# # TODO: report上报并展示在前端

# # 原始语料采集存在DB中
# annotation_data = Annotate(raw_data) # 原始语料标注
# annotation_answer = Annotate(answer) # 自测、人工打分
# save_data_to_DB(DB_interface, scores) # 评测记录存储