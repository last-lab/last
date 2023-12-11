from last.types.dataset import Dataset, QARecord, Message, MessageRole
from last.types.llm import LLM, LLMType
from last.types.plan import EvaluationType, Plan
from last.types.public import ID, Placeholder
from last.types.task import Task
from tqdm import tqdm
import re
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
        ## sheet_name 作为 theme, 确定 type_prompt
        sheet_name = Message(role=MessageRole.Chat, content=qa_record.sheet_name)
        await taskList.append(asyncio.create_task(critic_model(question, response, correct_ans, sheet_name)))
    
    # 无异常抛出的情况下 critic_list 与 task_list 元素一一对应
    critic_list = await taskList.get_result_list()
    progress_bar.update(1)
    print(llm_model.name + "的评测进度:评判模型评测完毕")

    # 处理评测结果
    for (dataset, qa_record), response, critic_str in zip(plan, response_list, critic_list):
        question = qa_record.question
        sheet_name = qa_record.sheet_name
        critic, reason= parse_critic_and_reason(str(critic_str))
        new_qa_record = QARecord(sheet_name=sheet_name, question=question, answer=response, critic=critic, reason=reason)
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

def parse_critic_and_reason(text: Message):
    text = str(text)
    # reason = 'None'
    critic = 'None'
    # reason_pattern = r'判断理由：(.*)'
    # reason_match = re.search(reason_pattern, text)
    # if reason_match:
    #     reason = reason_match.group(1)  
        
    # 提取评判结果
    result_pattern = r"判断结果：(\d+)(\n)?(\n)?判断理由"
    result_match = re.search(result_pattern, text)
    if result_match:
        critic = result_match.group(1)
        
    reason = text
    critic = Message(role=MessageRole.Chat, content=critic)
    return critic, reason

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
    # 每轮任务执行进度条
    # 每个 batch 完成后更新
    process_bar: tqdm
    
    def __init__(self):
        self.task_list = []
        self.result_list = []
        
        # core_count = multiprocessing.cpu_count()
        # self.task_batch_size = 2 * core_count
        # TODO: 不同LLM平台QPS不同，当前设为 4 是参照bilibili平台和huazang平台的QPS
        self.task_batch_size = 4
        
        self.process_bar = tqdm(desc="query task", leave=False)

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
            # a batch task accomplished
            # update process bar
            self.process_bar.update(len(self.task_list))

            self.task_list.clear()
            # update result list 
            self.result_list += temp_result_list

    async def get_result_list(self):
        # 所有任务均提交给TaskList
        # 检查并处理剩余 task
        if(len(self.task_list) > 0):
            await self.process_task()
        # 关闭并重置进度条
        self.process_bar.close()
        self.process_bar = tqdm(desc="query task", leave=False)
        return self.result_list.copy()

    def clear(self):
        self.task_list.clear()
        self.result_list.clear()