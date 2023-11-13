import os
import requests
import json
import time
from last.query.scheduler import http_request_with_callback, load_scheduler, shutdown_scheduler, get_response_with_id, waiting_task_queue_put
from last.query.task import Task
import last.query.test_data as test_data

def callback_func_test(response):
    """ http 请求完成后调用的回调函数
        首个参数 必须为 response

    Args:
        response (requests.Response): http response
    """
    ## process response
    pass
    
def test_query_callbackfunc():
    ## 启动 scheduler 线程
    load_scheduler()
    
    for request in test_data.reqs:
        # 通过 scheduler 发起请求
        # request = {"url": url, "headers": headers, "data": json.dumps(payload)}
        http_request_with_callback(request = request, callback_func = callback_func_test)        
    assert True
