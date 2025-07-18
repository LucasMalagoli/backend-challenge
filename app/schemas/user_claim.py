from pydantic import BaseModel
from typing import Optional


class UserClaimCreate(BaseModel):
    user_id: int
    claim_id: int


class UserClaimOut(BaseModel):
    user_id: int
    claim_id: int


class UserClaimUpdate(BaseModel):
    user_id: Optional[int]
    claim_id: Optional[int]
