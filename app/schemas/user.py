import string
import secrets
from datetime import date

from pydantic import BaseModel, EmailStr, field_validator, model_validator
from typing import List, Optional

from app.database import SessionLocal
from app.models.role import Role
from app.models.user import User
from app.schemas.claim import ClaimOut
from app.schemas.role import RoleOut


class UserBase(BaseModel):
    name: str
    email: EmailStr
    role_id: int


class UserCreate(UserBase):
    created_at: Optional[date] = date.today()
    password: Optional[str] = None
    claim_ids: Optional[List[int]] = []

    @classmethod
    def generate_random_password(cls, length: int = 12) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    @model_validator(mode='before')
    def set_password(cls, values):
        if not values.get('password'):
            values['password'] = cls.generate_random_password()
        return values

    @field_validator('role_id')
    def validate_role_id(cls, role_id):
        db = SessionLocal()
        role_exists = db.query(Role).filter(Role.id == role_id).first()
        db.close()
        if not role_exists:
            raise ValueError(f"Role with id {role_id} does not exist.")
        return role_id

    @field_validator('email')
    def validate_unique_email(cls, email):
        db = SessionLocal()
        try:
            if db.query(User).filter(User.email == email).first():
                raise ValueError(f"email {email} already registered")
        finally:
            db.close()
        return email


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    claim_ids: Optional[List[int]] = None

    @field_validator('role_id')
    def validate_role_id(cls, role_id):
        if role_id is None:
            return role_id

        db = SessionLocal()
        role_exists = db.query(Role).filter(Role.id == role_id).first()
        db.close()
        if not role_exists:
            raise ValueError(f"Role with id {role_id} does not exist.")
        return role_id


class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleOut
    claims: List[ClaimOut] = []

    class Config:
        from_attributes = True
