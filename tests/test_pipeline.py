# TODO client的部分、ORM的部分没有实现，LLM的调用是MOCK的
import os

from last.types.dataset import Dataset, QARecord
from last.types.llm import LLM, LLMType
from last.types.plan import EvaluationType, Plan
from last.types.public import ID, RiskDimension
from last.types.task import Task


def test_pipeline():
    # 如果需要加载新数据集, 则提供file\url，返回数据集对象
    file1_path = os.path.join("docs", "examples", "testset1.csv")
    dataset1 = Dataset(
        name="test1",
        focused_risks=[RiskDimension(level=1, name="国家安全")],
        file=file1_path,
    )

    # 上传第二份数据集
    file2_path = os.path.join("docs", "examples", "testset2.csv")
    dataset2 = Dataset(
        name="test2",
        focused_risks=[RiskDimension(level=1, name="个人隐私")],
        file=file2_path,
    )
    # 明确评测方案，即使用哪些数据集合集进行评测
    plan = Plan(
        name="union",
        eval_type=EvaluationType.auto_ai_critique,
        datasets=[dataset1, dataset2],
    )

    # 配置待测模型API
    llm_model = LLM(
        model_type=LLMType.normal,
        endpoint="https://puyu.openxlab.org.cn/puyu/api/v1/chat/completion",
        access_key="xxx",
    )

    if plan.eval_type == EvaluationType.auto_ai_critique:
        # 如果是AI测评，配置评分模型API
        critic_model = LLM(
            model_type=LLMType.critic,
            endpoint="https://puyu.openxlab.org.cn/puyu/api/v1/chat/completion",
            access_key="xxx",
        )
    # else:
    #   如果是人工测评，则新建标注模块
    #     critic_model = Annotation()

    new_qa_records = {}
    for qa_record in plan:  #
        question, correct_ans = qa_record.question, qa_record.answer
        responce = llm_model(question)
        score = critic_model(responce, correct_ans)
        new_qa_record = QARecord(question=question, answer=responce, score=score)
        new_qa_records[ID()] = new_qa_record

    # 上传本次评测记录, 返回评测报告和对话记录
    task = Task(
        plan=plan,
        llm_model=llm_model,
        critic_model=critic_model,
        results=new_qa_records,
    )

    # 保存评测报告到本地
    task.render_report(file_path="xxx", type="pdf")
    # 上传评测QA历史到数据库
    new_dataset = Dataset(
        name="test1",
        focused_risks=[RiskDimension(name="国家安全"), RiskDimension(name="个人隐私")],
        qa_records=new_qa_records,
    )

    assert new_dataset is not None
