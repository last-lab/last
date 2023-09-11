""" 
测试评测记录界面的所有功能

"""

from last.types.task import Task
from last.types.model import Model
from last.types.report import Report
from last.types.dataset import Dataset


with last.Client(name='puan', server_address="http://localhost:5000") as client:
    # 先查询目前已有的评测记录，数据来源是mock数据，

    # 新建评测
    dataset_list = []
    ## 明确评测方案，即使用哪些数据集进行评测
    task = Task(name="xxx", eval_type='auto', datasets=dataset_list)
    # 配置评测模型API 
    model = Model(endpoint="xxx", access_key='xxx', secret_key='xxx') 


    # for msg in task:
    # 执行一次评测任务, 返回评测结果 
    report, QAs = Report(task, model, verbose=True)  # if return_detail, return all response

    # 保存评测报告到本地
    report.render(file_path='xxx', type='pdf') 


    # 查看评测记录和评测报告

