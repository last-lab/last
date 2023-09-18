# TODO client的部分、ORM的部分没有实现，LLM的调用是MOCK的
import json
import os
import inspect

from last.client import Client

from last.types.dataset import Dataset, QARecord
from last.types.llm import LLM, LLMType
from last.types.plan import EvaluationType, Plan
from last.types.public import ID, RiskDimension, Placeholder
from last.types.task import Task

# 一个task需要plan+model，plan需要dataset


def test_create_eval():
    kwargs_json = json.dumps(
        {
            "$datasets": [
                {
                    "name": "test1",
                    "file": os.path.join("docs", "examples", "testset1.csv"),
                },
                {
                    "name": "test2",
                    "file": os.path.join("docs", "examples", "testset2.csv"),
                },
            ],
            "$llm_model": {"name": "PuYu", "endpoint": "xxx", "access_key": "xxx"},
            "$critic_model": {
                "name": "GPT-3.5-Turbo",
                "endpoint": "xxx",
                "access_key": "xxx",
            },
            "$plan": {"name": "SafetyTest"},
        }
    )
    Client.execute(AI_eval, kwargs_json)


def AI_eval(
    datasets=Placeholder(parser=lambda x: x),
    llm_model=Placeholder(parser=lambda x: x),
    critic_model=Placeholder(parser=lambda x: x),
    plan=Placeholder(parser=lambda x: x),
):
    from functools import reduce
    from operator import add    
    datasets = [
        Dataset(
            name=dataset['name'],
            file=dataset['file'],
        )
        for dataset in datasets
    ]

    
    plan = Plan(
        name=plan['name'], eval_type=EvaluationType.auto_ai_critique, datasets=datasets, focused_risks=reduce(add, [dataset.focused_risks for dataset in datasets])
    )

    llm_model = LLM(
        name=llm_model['name'], model_type=LLMType.normal, endpoint=llm_model['endpoint'], access_key=llm_model['access_key']
    )

    if plan.eval_type == EvaluationType.auto_ai_critique:
        critic_model = LLM(
            name=critic_model['name'],
            model_type=LLMType.critic,
            endpoint=critic_model['endpoint'],
            access_key=critic_model['access_key'],
        )

    new_qa_records = {}
    for qa_record in plan:  #
        question, correct_ans = qa_record.question, qa_record.answer
        responce = llm_model(question)
        score = critic_model(responce, correct_ans)
        new_qa_record = QARecord(question=question, answer=responce, score=score)
        new_qa_records[ID()] = new_qa_record

    task = Task(
        plan=plan,
        llm_model=llm_model,
        critic_model=critic_model,
        results=new_qa_records,
    )

    new_dataset = Dataset(
        name=plan.name,
        qa_records=new_qa_records,
    )

    return task, new_dataset
