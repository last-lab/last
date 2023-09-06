""" For TY & YC
load types and client

clients'admin served at services.

"""

from last.types import EvaluatedContext

# 采集->标注->训练->自测->采集 完成循环
raw_data = load_evaluationset("set_name/uuid", "services_address") #TODO: services启动，注册数据集
results = Report(raw_data) # 评测结果
# TODO：progress上报
for dim, question in raw_data:
    answer = model.infer(toxic_question) # 模型API推理
    results.add(dim, question, answer) # 评测结果
# TODO: report上报并展示在前端

# 原始语料采集存在DB中
annotation_data = Annotate(raw_data) # 原始语料标注
annotation_answer = Annotate(answer) # 自测、人工打分
save_data_to_DB(DB_interface, scores) # 评测记录存储