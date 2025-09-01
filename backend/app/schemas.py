from pydantic import BaseModel
from datetime import datetime
from typing import Any, List, Dict

class RequestCreate(BaseModel):
    user_id: int
    user_request: str
    messages: List[Dict[str, Any]]
    response: Any | None = None

class RequestOut(RequestCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
