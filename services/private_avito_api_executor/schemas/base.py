"""
Basic schemas.
"""
from enum import Enum

from pydantic import BaseModel


class AvitoResponseStatus(Enum):
    OK = 'ok'
    INCORRECT_DATA = 'incorrect-data'


class BaseAvitoResponse(BaseModel):
    status: AvitoResponseStatus
