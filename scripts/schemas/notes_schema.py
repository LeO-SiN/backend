from typing import Optional
from pydantic import BaseModel

class NotesSchema(BaseModel):
    title: str
    description: str
    tag : str