import os

from last.types.dataset import Dataset, QARecord
from last.types.llm import LLM, LLMType
from last.types.plan import EvaluationType, Plan
from last.types.public import ID, RiskDimension, Placeholder
from last.types.task import Task


def AI_eval():
    file1_path = Placeholder(parser=lambda x: x)
    dataset1 = Dataset(
        name="test1",
        focused_risks=[RiskDimension(level=1, name="国家安全")],
        file=file1_path,
    )
    dataset2 = Dataset(
        name="test2",
        focused_risks=[RiskDimension(level=1, name="个人隐私")],
        file=file1_path,
    )
    plan = Plan(
        name="union", eval_type=EvaluationType.auto_ai_critique, datasets=[dataset1, dataset2]
    )

    
    llm_model = LLM(model_type=LLMType.normal, endpoint="xxx", access_key="xxx", secret_key="xxx")

    if plan.eval_type == EvaluationType.auto_ai_critique:
        critic_model = LLM(
            model_type=LLMType.critic, endpoint="xxx", access_key="xxx", secret_key="xxx"
        )

    new_qa_records = {}
    for qa_record in plan:  #
        question, correct_ans = qa_record.question, qa_record.answer
        responce = llm_model(question)
        score = critic_model(responce, correct_ans)
        new_qa_record = QARecord(question=question, answer=responce, score=score)
        new_qa_records[ID()] = new_qa_record


    task = Task(plan=plan, llm_model=llm_model, critic_model=critic_model, results=new_qa_records)


    task.render_report(file_path="xxx", type="pdf")

    new_dataset = Dataset(
        name="test1",
        focused_risks=[RiskDimension(name="国家安全"), RiskDimension(name="个人隐私")],
        qa_records=new_qa_records,
    )


