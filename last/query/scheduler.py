import time
import threading
from queue import Queue, Empty
import requests
import json
import os
from aiohttp import web
import aiohttp
import asyncio
from last.query.id_generator import IDGenerator
import multiprocessing
from last.query.task import Task
from functools import partial

"""
TODO: NULL
"""

def schedule_requests():
    """
    scheduler 线程的任务
    调度请求的函数

    """
    while True:
        if not waiting_task_queue.empty():
            # 从请求队列中获取请求
            request_task = waiting_task_queue.get()
            # 处理请求
            future = executor.submit(process_request, request_task)
            if request_task._auto_task:
                #
                # 用 lambda f 方式传递 future 即 process_request 的 返回值
                # 将 request_task = request_task 作为默认参数传递给了回调函数的 lambda 表达式
                # 保证每次迭代中 捕获 当前循环的 request_task 值，并将其作为 参数 传递给 回调函数
                # 避免在循环中 注册 的 回调函数（_callback_func）引用 了循环变量 request_task
                # 由于循环迭代速度很快，当回调函数被调用时，循环已经完成或者正在循环，此时 request_task 的值被当前迭代的值所覆盖
                # 用 闭包来确保每个 回调函数 引用 的是正确的 request_task 对象
                #
                future.add_done_callback(lambda f, request_task = request_task: request_task._callback_func(f.result()))
                ## 替代写法
                # future.request_task = request_task
                # future.add_done_callback(lambda f: f.request_task._callback_func(f.result()))

# 处理请求任务的调度线程
_scheduler = threading.Thread(target=schedule_requests)

import concurrent.futures

# response buffer size
BUFFER_SIZE = 1024

# request worker thread pool
# I/O 密集操作
executor = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() * 2)

# 创建 未完成任务队列 和 响应缓冲区 (dict)
# 待处理请求任务队列
# element: class task
waiting_task_queue = Queue()
# 已完成请求任务队列
# element: class task
completed_task_queue = Queue()
# request buffer
# key: int; taks id;
# element: class task;
completed_task_dict = dict()

# 线程锁
waiting_task_queue_lock = threading.Lock()
completed_task_dict_lock = threading.Lock()

# completed task buffer 剩余空间
completed_task_count_semaphore = threading.Semaphore(BUFFER_SIZE)
# completed task 未处理响应
completed_task_fill_count_semaphore = threading.Semaphore(0)

def process_request(request_task):
    """
    处理请求的函数

    Args:
        request: 请求对象
    """
    current_thread = threading.current_thread()
    thread_id = current_thread.ident
    # 查看实际 处理 task 线程
    # print(f"Current Thread ID: {thread_id}")
    
    # 发送请求并处理响应
    request = request_task._request
    request_task._response = requests.post(request["url"], headers = request["headers"], data = request["data"])
    if(not request_task._auto_task):
        ## target 不立即取回 response 时，存放在 waiting_task_queue 中
        with completed_task_dict_lock:
            # 处理完请求后将 响应 放入 响应缓冲区 中
            completed_task_count_semaphore.acquire()
            completed_task_dict[request_task._id] = request_task
            completed_task_fill_count_semaphore.release()
    # return object, 作为 回调函数实参
    return request_task._response

def waiting_task_queue_put(request, callback_func = None, auto_task = True,target = None):
    """ 向 waiting_task_queue 添加元素

    Args:
        request (requests): 目前是query request
        callback_func (function): HTTPPAPILLMModel _callback_func
    """    
    
    req_task = Task(request, callback_func = callback_func, auto_task = auto_task, target = target)

    with waiting_task_queue_lock:
            waiting_task_queue.put(req_task)
    return req_task
            
def get_response_with_id(id):
    """ 阻塞方式获取response
    ## TODO: 阻塞是否已满足业务需求
    Args:
        id (int): task id
    """    
    with completed_task_dict_lock:
        try:
            return completed_task_dict[id]._response
        except:
            pass
    
def load_scheduler():
    """ 启动 scheduler 线程
    """    
    try:
        global _scheduler
        if _scheduler and not _scheduler.is_alive():
            # the threading scheduler not null and not alive
            _scheduler.start()
    except Exception as e:
        print(str(e))
        pass

def shutdown_scheduler():
    """ 停止 scheduler 线程
    """    
    try:
        global _scheduler
        if _scheduler:
            _scheduler.stop()
    except:
        pass