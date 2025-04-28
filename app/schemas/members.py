from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date


class MemberBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None
    active: bool = True


class MemberCreate(MemberBase):
    pass


class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    active: Optional[bool] = None


class MemberResponse(MemberBase):
    id: int
    registration_date: date

    class Config:
        from_attributes = True
        populate_by_name = True