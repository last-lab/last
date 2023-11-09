import requests
from id_generator import IDGenerator
        
class Task(object):
    """
    """
    ## task ID
    ## from id_generator
    _id: int
    ##
    _request: requests
    ##
    _response: requests.Response
    ## call back function
    _call_back_func: None
    
    
    ## create request task
    def __init__(self, response, call_back_func):
        self._response = response
        self._call_back_func = call_back_func
        
        _idGenerator = IDGenerator()
        self._id = _idGenerator.get_id()
        