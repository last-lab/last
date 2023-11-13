import os
import requests
import json
import time
from last.query.scheduler import waiting_task_queue_put, load_scheduler, shutdown_scheduler, get_response_with_id
from last.query.task import Task
import last.query.test_data as test_data

""" 
    demo
"""

# start = time.time()

# class TestScheduler(unittest.TestCase):
class TestScheduler():
    def __init__(self):
        self._taskID = []
    
    def __del__(self):
        pass
    
    def _callback_func(self, response):
        print(response.json())
        # print("duration : {:.2f}".format(time.time()- start))
    
    ## 模拟class LLM query
    ## 回调方式获取response
    def query_callbackfunc(self):
        # start = time.time()
        for req in test_data.reqs:
            ## 发起 request
            ## request = {"url": url, "headers": headers, "data": json.dumps(payload)}
            ## callback_func 含 response 形参的回调函数
            waiting_task_queue_put(request = req, callback_func = self._callback_func)
    
    ## 模拟class LLM query
    ## response 暂存 scheduler 的 response buffer
    ## 需 target 自己从 response buffer 获取 response
    def query_no_callbackfunc(self):
        for req in test_data.reqs:
            ## 发起 request
            ## request = {"url": url, "headers": headers, "data": json.dumps(payload)}
            ## 无callback_func 需设置 auto_task = False
            waiting_task_queue_put(request = req, auto_task = False)

    ## 从 response buffer 获取 response
    def get_response(self):
        pass
    
def test_query_callbackfunc():
    ## 启动 scheduler 线程
    load_scheduler()
    ## 某个有 query 需求的对象
    test = TestScheduler()
    #
    test.query_callbackfunc()
    #
    # test.query_no_callbackfunc()

    ## 某个有 query 需求的对象
    test2 = TestScheduler()
    test2.query_callbackfunc()
        



