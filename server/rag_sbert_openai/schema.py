from pydantic import BaseModel
from typing import Any, Dict, List


class Output(BaseModel):
    execution_time: float
    context: str
    answer: str