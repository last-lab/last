import time
import threading
from queue import Queue, Empty
import requests
import json
import os
from aiohttp import web
import aiohttp
import asyncio
from id_generator import IDGenerator
import multiprocessing
from last.query.task import Task

# 处理请求任务的调度线程
_scheduler: threading

import concurrent.futures

# response buffer size
BUFFER_SIZE = 1024

# request worker thread pool
# I/O 密集操作
executor = concurrent.futures.ThreadPoolExecutor(max_workers=multiprocessing.cpu_count() * 2)
# 创建请求队列和响应队列
# 待处理请求任务队列
# element: class task
waiting_task_queue = Queue()
# 已完成请求任务队列
# element: class task
completed_task_queue = Queue()

# 创建线程锁和条件变量
waiting_task_queue_lock = threading.Lock()

completed_task_queue_lock = threading.Lock()
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
    print(f"Current Thread ID: {thread_id}")
    
    # 发送请求并处理响应
    request_task._response = requests.post(url, headers = headers, data = json.dumps(payload))
    # print(response.json())
    with waiting_task_queue_lock:
        # 标记请求队列任务完成
        waiting_task_queue.task_done()
    # 处理完请求后将响应放入响应队列
    # response = f"Response for request {request}"
    completed_task_count_semaphore.acquire()
    completed_task_queue.put(request_task)
    # 通知主线程有新的响应
    # TODO: 主线程 的callback 可以按照需求是立即处理 completed_task_queue 还是 暂时不处理completed_task_queue
    # 当前 设计为 主线程立即 处理completed_task_queue
    completed_task_fill_count_semaphore.release()

def schedule_requests():
    """
    调度请求的函数

    """
    while True:
        if not waiting_task_queue.empty():
            # 从请求队列中获取请求
            request_task = waiting_task_queue.get()
            # 处理请求
            ft = executor.submit(process_request, request_task)
            ft.add_done_callback(callback_func_test)

def callback_func_test(future):
    print("Callback")
    acquired = completed_task_fill_count_semaphore.acquire(blocking=False)
    if acquired:
        try:
            response_task = completed_task_queue.get()
            print(response_task._response.json())
            completed_task_queue.task_done()
        # except Empty:
        #     # # get 不到抛出 Empty
        #     pass
        finally:
            completed_task_count_semaphore.release()
    else:
        # 未获取到信号量，执行其他操作或报错
        pass


def waiting_task_queue_put(request, callback_func):
    """ 向 waiting_task_queue 添加元素

    Args:
        request (requests): 目前是query request
        callback_func (function): HTTPPAPILLMModel _callback_func
    """    
    req_task = Task(req, callback_func)
    with waiting_task_queue_lock:
            waiting_task_queue.put(req_task)

def load_scheduler():
    try:
        if not _scheduler:
            _scheduler = threading.Thread(target=schedule_requests)
        _scheduler.start()
    except:
        pass

def shutdown_scheduler():
    try:
        if _scheduler:
            _scheduler.stop()
    except:
        pass