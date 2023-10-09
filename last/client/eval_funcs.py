from last.types.dataset import Dataset, QARecord
from last.types.llm import LLM, LLMType
from last.types.plan import EvaluationType, Plan
from last.types.public import ID, Placeholder, RiskDimension
from last.types.task import Task
import json
import asyncio

async def AI_eval(
    datasets=Placeholder(parser=lambda x: x),
    llm_model=Placeholder(parser=lambda x: x),
    critic_model=Placeholder(parser=lambda x: x),
    plan=Placeholder(parser=lambda x: x),
):
    datasets = [
        Dataset(
            name=dataset["name"],
            file=dataset["file"],
        )
        for dataset in datasets
    ]

    plan = Plan(
        name=plan["name"],
        eval_type=EvaluationType.auto_ai_critique,
        datasets=datasets,
    )

    llm_model = LLM(
        name=llm_model["name"],
        model_type=LLMType.normal,
        endpoint=llm_model["endpoint"],
        access_key=llm_model["access_key"],
    )

    if plan.eval_type == EvaluationType.auto_ai_critique:
        critic_model = LLM(
            name=critic_model["name"],
            model_type=LLMType.critic,
            endpoint=critic_model["endpoint"],
            access_key=critic_model["access_key"],
        )

    new_qa_records = {}
    for qa_record in plan:  
        question, correct_ans = qa_record.question, qa_record.answer
        responce = await llm_model(question)
        critic = await critic_model(responce, correct_ans)
        new_qa_record = QARecord(question=question, answer=critic, critic=critic)
        new_qa_records[ID()] = new_qa_record

    task = Task(
        plan=plan,
        llm_model=llm_model,
        critic_model=critic_model,
        results=new_qa_records,
    )

    new_dataset = Dataset(name=plan.name, qa_records=new_qa_records, file=None)

    return task, new_dataset
