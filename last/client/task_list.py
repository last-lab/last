from last.types.dataset import Dataset, QARecord, Message, MessageRole
from last.types.llm import LLM, LLMType
from last.types.plan import EvaluationType, Plan
from last.types.public import ID, Placeholder
from last.types.task import Task
from tqdm import tqdm
import re
import asyncio

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