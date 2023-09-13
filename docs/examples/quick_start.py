""" For TY & YC
load types and client

clients'admin served at services.

"""

from last.client import client_wrapper
from last.types.plan import Plan, EvaluationType
from last.types.llm import LLM, LLMType
from last.types.task import Task
from last.types.dataset import Dataset
from last.types.public import RiskDimension

# Main Flow
with client_wrapper(name='puan', server_address="http://localhost:5020") as client: # TODO 目前还没实现client作为全局变量
    # 如果需要加载新数据集, 则提供DatasetInfo，内含数据集访问链接，返回dataset uid="uuid4"
    dataset1 = Dataset(name="test1", dimensions=[RiskDimension(name="国家安全")], file='docs/examples/testset.csv')
    # 上传第二份数据集
    dataset2 = Dataset(name="test2", dimensions=[RiskDimension(name="个人隐私")], file='docs/examples/testset.csv')
    # 明确评测方案，即使用哪些数据集进行评测
    plan = Plan(name="union", eval_type=EvaluationType.auto_ai_critique, datasets=[dataset1,dataset2])

    # 配置待测模型API
    llm_model = LLM(model_type=LLMType.normal, endpoint="xxx", access_key='xxx', secret_key='xxx') 

    if plan.eval_type == EvaluationType.auto_ai_critique:
        # 如果是AI测评，配置评分模型API
        critic_model = LLM(model_type=LLMType.critic, endpoint="xxx", access_key='xxx', secret_key='xxx')   
    # else:
    #   如果是人工测评，则新建标注模块
    #     critic_model = Annotation()


    scores = []
    responces = []
    for qa_record in plan: # 
        question, correct_ans = qa_record.question, qa_record.answer
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




