import time

## LAST 初始时间戳
POCH = 1699241998826

## 64位ID的划分
TIMESTAMP = 52
SEQUENCE_BITS = 12

## 位偏移
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS

# 序号循环掩码
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

class IDGenerator(object):
    """ Singleton """
    """ Simple snowflake ID"""
    """ Generate ID for chat query. """
    """ Timestamp : 52bit (higher)"""
    """ Different ids generated within the current millisecond: 12bit (lower)"""
    
    _instance = None
    def __new__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kw)
        cls.last_timestamp = -1    ## 上一次计算的时间戳
        return cls._instance

    def __init__(self):
        pass
    
    def _gen_timestamp(self):
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)
    
    def get_id(self):
        """
        获取新ID
        :return:
        """
        timestamp = self._gen_timestamp()
        
        ## 时钟回拨
        if timestamp < self.last_timestamp:
            raise
        
        if timestamp == self.last_timestamp:
            ## 在同一个毫秒区间内
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            ## 新的毫秒区间
            self.sequence = 0
        
        self.last_timestamp = timestamp
        
        new_id = ((timestamp - POCH) << TIMESTAMP_LEFT_SHIFT) | self.sequence
        return new_id
        
        