# Change will be in the future
# Future changes will be made to this file
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    publication_year: Optional[int] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    available: bool = True


class BookCreate(BookBase):
    pass # in furture


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    genre: Optional[str] = None
    description: Optional[str] = None
    available: Optional[bool] = None


class BookResponse(BookBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        populate_by_name = True