from typing import Optional

from pydantic import BaseModel


class ClaimCreate(BaseModel):
    description: str
    active: Optional[bool] = True


class ClaimOut(BaseModel):
    id: int
    description: str
    active: Optional[bool] = True

    class Config:
        from_attributes = True


class ClaimUpdate(BaseModel):
    description: Optional[str]
    active: Optional[bool]
