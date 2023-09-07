from dataclasses import dataclass
from typing import List, Dict, Union, Optional
from pydantic import BaseModel


@dataclass
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

class DateString:
    def __init__(self, date_str):
        self.date_str = date_str

    def to_datetime(self):
        return datetime.strptime(self.date_str, "%Y-%m-%d")

    def format(self, format_str):
        date_obj = self.to_datetime()
        return date_obj.strftime(format_str)

    def add_days(self, days):
        date_obj = self.to_datetime()
        new_date = date_obj + timedelta(days=days)
        return DateString(new_date.strftime("%Y-%m-%d"))

    def __str__(self):
        return self.date_str

@dataclass
class UserInfo(BaseModel):
    id: str 
    name: str
    email: str
    created_at: DateString # yyyy-MM-dd HH:mm:ss
    permission: PermissionLevel


class CodeMsg:
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"Error {self.code}: {self.message}"


class ReturnCode:
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



