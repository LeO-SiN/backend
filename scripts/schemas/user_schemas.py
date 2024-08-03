from typing import Any, Optional
from pydantic import BaseModel, EmailStr


class UserRequestSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class DefaultResponse(BaseModel):
    status: str = "Failed"
    message: Optional[str]
    data: Optional[Any]


class ResponseModel(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True
