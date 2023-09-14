from typing import List, Dict, Union, Optional
from pydantic import BaseModel, Field
from enum import Enum, auto
from datetime import datetime
import uuid


class RiskDimension(BaseModel):
    level: Optional[int] = Field(default=1)  # 风险类型级别，默认是三级
    name: str
    description: Optional[str] = None
    uplevel_risk_name: Optional[str] = Field(default=None)

    def __str__(self):
        return self.name


class PermissionLevel(Enum):
    SUPER_ADMIN = auto()
    ADMIN = auto()
    EDITOR = auto()
    OPERATOR = auto()
    VIEWER = auto()


class DateString(BaseModel):  # 改成时间戳
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
    code: int
    message: str

    def __str__(self):
        return f"Error {self.code}: {self.message}"


class ReturnCode(Enum):
    NOT_FOUND = CodeMsg(code=404, message="Not found")
    UNAUTHORIZED = CodeMsg(code=401, message="Unauthorized")
    FORBIDDEN = CodeMsg(code=403, message="Forbidden")
    SUCCESS = CodeMsg(code=10000, message="Success")
    BAD_REQUEST = CodeMsg(code=400, message="Bad Request")
    INVALID_INPUT = CodeMsg(code=422, message="Invalid Input")
    ALREADY_EXIST = CodeMsg(code=101, message="Already Exist")
    

    def __str__(self):
        return str(self.value)


class StateCode(Enum):
    In_Progress = CodeMsg(code=0, message="进行中")
    Done = CodeMsg(code=1, message="已完成")
    Error = CodeMsg(code=-1, message="异常")

    def __str__(self):
        return str(self.value)


class ID(str):
    def __new__(cls):
        return super().__new__(cls, uuid.uuid4())
