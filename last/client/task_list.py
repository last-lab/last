from last.types.dataset import Dataset, QARecord
from last.types.llm import LLM, LLMType
from last.types.plan import EvaluationType, Plan
from last.types.public import ID, Placeholder, RiskDimension
from last.types.task import Task
from tqdm import tqdm
import json
import asyncio
import multiprocessing

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
    
    ## TODO: 对每个失败的 task 使用 0 并发的方式处理, 策略是在每一 batch task 完成后检查result，立即对error的task进行处理
    # 因为出现error说明并发过高，停止batch task，使用 0 并发的方式处理 error task，降低并发量
    
    def __init__(self):
        self.task_list = []
        self.result_list = []
        
        # core_count = multiprocessing.cpu_count()
        # self.task_batch_size = 2 * core_count
        
        # TODO: 限制峰值 QPS; ( 研究如何保证 avg_RPS --> QPS, 当前 avg_QPS == 单个请求耗时 / task_batch_size, 是否有multi / async + 时序 的方法
        # 注意, task_batch_size <= QPS, 否则服务大概率返回5xx
        self.task_batch_size = 4
        
        self.process_bar = tqdm(desc="query task", leave=False)

    # 接收任务
    async def append(self, task: asyncio.Task):
        self.task_list.append(task)
        # 任务数量达到 阈值 触发任务处理行为
        if(len(self.task_list) > self.task_batch_size):
            await self.process_task()

    # 通过检查请求返回值 检查task是否成功
    def check_single_error_task(self, result):
        # 检查 status 是否是 5xx 
        if "status" not in result or result["status"] != 0:
            return False
        return True
    
    # 检查一批result
    def check_list_error_task(self, result_list: list) -> bool:
        self.error_tasks_index_list = list(map(self.check_single_error_task, result_list))
        return all(self.error_tasks_index_list)
    
    async def process_single_task(self):
        
        pass
    
    async def process_error_task(self, tasks: list, results: list, error_tasks_index: list):
        # tasks、results、error_tasks_index 均添加到 self中
        pass
    
    
    # 处理任务 更新 result_list
    async def process_task(self):
        if(len(self.task_list) > 0):
            temp_result_list = await asyncio.gather(*(self.task_list))
            while self.check_list_error_task(self, temp_result_list):
                self.process_error_task()
                pass
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