import requests
from last.query.id_generator import IDGenerator
        
class Task(object):
    """ request task
        id: 
            int64;
            created from IDGenerator
            非回调方式获取完成的请求时, # TODO 可以通过id从completed_task_queue中获取response;  
        request: 
            requests;
        response: 
            requests.Response;
        callback_func: 
            function; 
            形参中包含 response 的回调函数;
        target: 
            object; 
            发送该任务的 object 指针 (闲置);
        auto_task: 
            boolean;
            默认 True;
                True: 回调直接获取 response;
                False: target 从completed_task_queue中获取;
    """
    ## create request task
    def __init__(self, request = None, callback_func = None, auto_task = True, target = None):
        _idGenerator = IDGenerator()
        self._id = _idGenerator.get_id()
        
        self._request = request
        
        self._callback_func = callback_func
        
        self._response = requests.Response()
        
        self._target = target
        
        self._auto_task = auto_task
