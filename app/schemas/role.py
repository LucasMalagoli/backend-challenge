from pydantic import BaseModel
from typing import Optional


class RoleCreate(BaseModel):
    description: str


class RoleOut(BaseModel):
    description: str
    id: int

    class Config:
        from_attributes = True


class RoleUpdate(BaseModel):
    description: Optional[str] = None
