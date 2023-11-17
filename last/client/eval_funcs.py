from last.types.dataset import Dataset, QARecord
from last.types.llm import LLM, LLMType
from last.types.plan import EvaluationType, Plan
from last.types.public import ID, Placeholder, RiskDimension
from last.types.task import Task
from tqdm import tqdm
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
    progress_bar = tqdm(total=None, desc=llm_model.name + "的评测进度", leave=False)
    
    # 任务队列
    taskList = TaskList()
    # 待测模型的回答
    response_list = []
    # 评测结果
    critic_list = []
    
    for qa_record in plan:
        question = qa_record.question
        await taskList.append(asyncio.create_task(llm_model(question)))
        
    # 无异常抛出的情况下 response_list 与 task_list 元素一一对应
    response_list = await taskList.get_result_list()
    progress_bar.update(1)
    progress_bar.set_description(llm_model.name + "的评测进度:待测模型测试完毕")
    
    # critic任务
    taskList.clear()
    for qa_record, response in zip(plan, response_list):
        question = qa_record.question
        correct_ans = qa_record.answer
        await taskList.append(asyncio.create_task(critic_model(question, response, correct_ans)))
    
    # 无异常抛出的情况下 critic_list 与 task_list 元素一一对应
    critic_list = await taskList.get_result_list()
    progress_bar.update(1)
    progress_bar.set_description(llm_model.name + "的评测进度:评判模型评测完毕")
    
    # 处理评测结果
    for qa_record, response, critic in zip(plan, response_list, critic_list):
        question = qa_record.question
        new_qa_record = QARecord(question=question, answer=response, critic=critic)
        new_qa_records[ID()] = new_qa_record
    progress_bar.update(1)
    progress_bar.set_description(llm_model.name + "的评测进度:评测结果处理完毕")
    progress_bar.close()

    task = Task(
        plan=plan,
        llm_model=llm_model,
        critic_model=critic_model,
        results=new_qa_records,
    )

    new_dataset = Dataset(name=plan.name + "+" + llm_model.name + "+问答记录", qa_records=new_qa_records, file=None)

    return task, new_dataset

class TaskList():
    """ 模拟任务队列 
        用于控制并发数量
    """ 
    # element: asyncio.Task
    task_list: list
    # task result
    # element: class Message
    result_list: list
    # 触发 process_task 的 阈值; 可并发数量
    task_batch_size: int
    def __init__(self):
        self.task_list = []
        self.result_list = []
        
        core_count = multiprocessing.cpu_count()
        self.task_batch_size = 2 * core_count

    # 接收任务
    async def append(self, task: asyncio.Task):
        self.task_list.append(task)
        # 任务数量达到 阈值 触发任务处理行为
        if(len(self.task_list) > self.task_batch_size):
            await self.process_task()

    # 处理任务 更新 result_list
    async def process_task(self):
        if(len(self.task_list) > 0):
            temp_result_list = await asyncio.gather(*(self.task_list))
            self.task_list.clear()
            self.result_list += temp_result_list

    async def get_result_list(self):
        # 处理剩余 task
        if(len(self.task_list) > 0):
            await self.process_task()
        return self.result_list.copy()

    def clear(self):
        self.task_list.clear()
        self.result_list.clear()