from typing import List, Dict, Union, Optional
from pydantic import BaseModel
from enum import Enum, auto
from datetime import datetime

class RiskDimension(BaseModel):
    level: int
    name: str
    description: str

    def __str__(self):
        return self.name


RelatedRiskDimensions = Dict[str, Dict[str, Dict[str, str]]]


class PermissionLevel(Enum):
    SUPER_ADMIN = auto()
    ADMIN = auto()
    EDITOR = auto()
    OPERATOR = auto()
    VIEWER = auto()



class DateString(BaseModel):
    year: str
    month: str
    day: str
    hour: str
    minute: str
    second: str

    def to_datetime(self):
        return datetime.strptime(self.__str__, "%Y-%m-%d %H:%M:%S")

    def format(self, format_str):
        date_obj = self.to_datetime()
        return date_obj.strftime(format_str)

    def __str__(self):
        return f"{self.year}-{self.month}-{self.day} {self.hour}:{self.minute}:{self.second}"


class UserInfo(BaseModel):
    id: str
    name: str
    email: str
    created_at: DateString  
    permission: PermissionLevel


class CodeMsg(BaseModel):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"Error {self.code}: {self.message}"


class ReturnCode(BaseModel):
    NOT_FOUND = CodeMsg(404, "Not found")
    UNAUTHORIZED = CodeMsg(401, "Unauthorized")
    FORBIDDEN = CodeMsg(403, "Forbidden")
    SUCCESS = CodeMsg(10000, "Success")
    BAD_REQUEST = CodeMsg(400, "Bad Request")
    INVALID_INPUT = CodeMsg(422, "Invalid Input")


class StateCode:
    In_Progress = CodeMsg(0, "进行中")
    Done = CodeMsg(1, "已完成")
    Error = CodeMsg(-1, "异常")
