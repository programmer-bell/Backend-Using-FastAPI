from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class LoanBase(BaseModel):
    book_id: int
    member_id: int
    loan_date: date = Field(default_factory=date.today)
    due_date: Optional[date] = None


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    return_date: Optional[date] = None


class LoanResponse(LoanBase):
    id: int
    return_date: Optional[date] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True


class LoanDetailResponse(LoanResponse):
    book_title: str
    member_name: str

    class Config:
        from_attributes = True
        populate_by_name = True