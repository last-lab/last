""" For TY & YC
load types and client

clients'admin served at services.

"""
import last
from last.client import Client
from last.types.plan import Plan, EvaluationType
from last.types.llm import LLM
from last.types.task import Task
from last.types.dataset import Dataset

# Main Flow
with Client(name='puan', server_address="http://localhost:5020") as client:
    # 如果需要加载新数据集, 则提供DatasetInfo，内含数据集访问链接，返回dataset uid="uuid4"
    dataset1 = Dataset(name="xxx", dimensions="国家安全", url='http://xxxxxx')
    # 上传第二份数据集
    dataset2 = Dataset(name="xxx", dimensions="个人隐私", url='http://xxxxxx')
    # 明确评测方案，即使用哪些数据集进行评测
    eval_type = EvaluationType.auto_ai_critique
    plan = Plan(name="xxx", eval_type='human', datasets=[dataset1,dataset2])

    # 配置待测模型API
    llm_model = LLM(endpoint="xxx", access_key='xxx', secret_key='xxx') 

    if eval_type == EvaluationType.auto_ai_critique:
        # 配置评分模型API
        critic_model = LLM(endpoint="xxx", access_key='xxx', secret_key='xxx', prompt_template="请根据语义的相似度比较以下，评分范围0.0~10.0：{}")   # TODO SystemMessage的支持
    # else:
    #     critic_model = Annotation()


    scores = []
    responces = []
    for question, correct_ans in plan:
        responce = llm_model(question)
        responces.append(responce)
        score = critic_model(responce, correct_ans)
        scores.append(score)


    # 上传本次评测记录, 返回评测结果 
    report, QAs = Task(plan, llm_model, scores, critic_model)  # if return_detail, return all response

    # 保存评测报告到本地
    report.render(file_path='xxx', type='pdf') 
    # 上传评测QA历史到数据库
    new_dataset = Dataset(QAs)



    # 对新的dataset创建一个标注任务




