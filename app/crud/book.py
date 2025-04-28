from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.models.models import Book
from app.schemas.book import BookCreate, BookUpdate


def get_book(db: AsyncSession, book_id: int):
    """Get a book by ID"""
    result = db.execute(select(Book).where(Book.id == book_id))
    return result.scalars().first()


def get_book_by_isbn(db: AsyncSession, isbn: str):
    """Get a book by ISBN"""
    result = db.execute(select(Book).where(Book.isbn == isbn))
    return result.scalars().first()


def get_books(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    author: Optional[str] = None,
    available: Optional[bool] = None,
):
    """Get all books with optional filtering"""
    query = select(Book)
    
    # Apply filters if provided
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if available is not None:
        query = query.filter(Book.available == available)

    query = query.offset(skip).limit(limit)
    result = db.execute(query)
    return result.scalars().all()


def create_book(db: AsyncSession, book: BookCreate):
    """Create a new book"""
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: AsyncSession, book_id: int, book: BookUpdate):
    """Update a book"""
    # Filter out None values
    update_data = {k: v for k, v in book.model_dump().items() if v is not None}
    if not update_data:
        return  get_book(db, book_id)
    
    db.execute(
        update(Book)
        .where(Book.id == book_id)
        .values(**update_data)
    )
    db.commit()
    return  get_book(db, book_id)


def delete_book(db: AsyncSession, book_id: int):
    """Delete a book"""
    book =  get_book(db, book_id)
    if book:
         db.execute(delete(Book).where(Book.id == book_id))
         db.commit()
    return book