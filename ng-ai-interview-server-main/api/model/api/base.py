from enum import Enum
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel
from datetime import datetime

T = TypeVar('T')

class ResponseCode(str, Enum):
    SUCCESS = "0"
    FAILED = "1"
    INVALID_PARAMS = "2"
    SYSTEM_ERROR = "500"

class Response(BaseModel, Generic[T]):
    code: str = ResponseCode.SUCCESS
    message: str = "success"
    data: Optional[T] = None 