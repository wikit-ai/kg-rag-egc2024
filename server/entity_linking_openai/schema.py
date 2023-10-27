from pydantic import BaseModel
from typing import Any, Dict, List


class Output(BaseModel):
    execution_time: float
    entities: Dict[str, Any]
    queries: List[str]
    context: str
    answer: str