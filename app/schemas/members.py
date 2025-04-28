# this file defines the Pydantic models for the members of the library system
# This schemas file defines the data models for the Member entity in a library management system.
# It includes the base model, create and update models, and response models for API interactions.

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