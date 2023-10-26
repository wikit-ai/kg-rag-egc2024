from pydantic import BaseModel
from typing import List

class WikitBotMessage(BaseModel):
    replies: List[str]

class WikitBotApiResponse(BaseModel):
    messages: List[WikitBotMessage]
