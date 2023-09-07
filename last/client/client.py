import contextlib
from contextlib import ContextDecorator, contextmanager

class Client(ContextDecorator):
    def __init__(self, name, server_address):
        self.name = name
        self.server_address = server_address

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # 离开上下文时，清除全局变量中的上下文信息
        self.disconnect()
        return False

    def connect(self):
        print(f"Connected to {self.name}")

    def disconnect(self):
        print(f"Disconnected from {self.name}")