from last.types.dataset import Dataset, QARecord
from last.types.llm import LLM, LLMType
from last.types.plan import EvaluationType, Plan
from last.types.public import ID, Placeholder, RiskDimension
from last.types.task import Task
from tqdm import tqdm
from task_list import TaskList
import json
import asyncio
import multiprocessing


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
    progress_bar = tqdm(total=3, desc=llm_model.name + "的评测进度", leave=False)
    
    # 任务队列
    taskList = TaskList()
    # 待测模型的回答
    response_list = []
    # 评测结果
    critic_list = []
    
    for dataset, qa_record in plan:
        question = qa_record.question
        await taskList.append(asyncio.create_task(llm_model(question)))
        
    # 无异常抛出的情况下 response_list 与 task_list 元素一一对应
    response_list = await taskList.get_result_list()
    progress_bar.update(1)
    print(llm_model.name + "的评测进度:待测模型测试完毕")
    
    # critic任务
    taskList.clear()
    for (dataset, qa_record), response in zip(plan, response_list):
        question = qa_record.question
        correct_ans = qa_record.answer
        await taskList.append(asyncio.create_task(critic_model(question, response, correct_ans)))
    
    # 无异常抛出的情况下 critic_list 与 task_list 元素一一对应
    critic_list = await taskList.get_result_list()
    progress_bar.update(1)
    print(llm_model.name + "的评测进度:评判模型评测完毕")

    # 处理评测结果
    for (dataset, qa_record), response, critic in zip(plan, response_list, critic_list):
        question = qa_record.question
        sheet_name = qa_record.sheet_name
        new_qa_record = QARecord(sheet_name=sheet_name, question=question, answer=response, critic=critic)
        new_qa_records[ID()] = new_qa_record
    progress_bar.update(1)
    print(llm_model.name + "的评测进度:评测结果处理完毕")
    progress_bar.close()

    task = Task(
        plan=plan,
        llm_model=llm_model,
        critic_model=critic_model,
        results=new_qa_records,
    )

    new_dataset = Dataset(name=plan.name + "+" + llm_model.name + "+问答记录", qa_records=new_qa_records, file=None)

    return task, new_dataset
