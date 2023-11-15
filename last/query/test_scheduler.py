import os
import requests
import json
import time
from last.query.scheduler import http_request_with_callback
from last.query.task import Task
import last.query.test_data as test_data
import pytest

_responses = []

def example_callback_func():
    """ http 请求完成后调用的回调函数
        首个参数 必须为 response

    Args:
        response (requests.Response): http response
    """
    _responses.append(response)
    
def example_query_callbackfunc():
    for request in test_data.reqs:
        # 通过 scheduler 发起请求
        # request = {"url": url, "headers": headers, "data": json.dumps(payload)}
        try:
            http_request_with_callback(request = request, callback_func = callback_func_test)
        except TypeError as e:
            print("Error caught in function callback_func:", e)


def test_http_request_with_callback_no_exception():
    def callback(request: requests):
        pass
    assert http_request_with_callback(request = test_data.reqs[0], callback_func = callback) is None
    
def test_http_request_with_callback_callback_type_mismatch():
    def callback(arg):
        pass
    
    with pytest.raises(TypeError, match="The parameter of the 'callback' function must be of type Request"):
        http_request_with_callback(request = test_data.reqs[0], callback_func = callback)
    
    
def test_http_request_with_callback_no_arg():
    def callback():
        pass
    
    with pytest.raises(TypeError, match="The 'callback' function must have exactly one parameter"):
        http_request_with_callback(request = test_data.reqs[0], callback_func = callback)