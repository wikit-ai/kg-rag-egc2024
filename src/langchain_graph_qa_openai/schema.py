from pydantic import BaseModel


class Output(BaseModel):
    execution_time: float
    query: str
    context: str
    answer: str
