from pydantic import BaseModel
from datetime import timedelta

class BlogBase(BaseModel):
    title: str
    content: str