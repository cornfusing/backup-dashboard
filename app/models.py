from pydantic import BaseModel
from typing import Optional


class EventIn(BaseModel):
    source: str
    event: str
    message: Optional[str] = None
