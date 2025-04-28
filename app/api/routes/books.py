from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.database.db import get_db
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.crud import book as book_crud

router = APIRouter(
    prefix="/books",
    tags=["books"],
)


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(
    book: BookCreate,
    db: AsyncSession = Depends(get_db)
):
    db_book = book_crud.get_book_by_isbn(db, isbn=book.isbn)
    if db_book:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book with ISBN {book.isbn} already exists"
        )
    return book_crud.create_book(db=db, book=book)


@router.get("/", response_model=List[BookResponse])
def read_books(
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    author: Optional[str] = None,
    available: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    books = book_crud.get_books(
        db, skip=skip, limit=limit, 
        title=title, author=author, available=available
    )
    return books


@router.get("/{book_id}", response_model=BookResponse)
def read_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_book = book_crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return db_book


@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookUpdate,
    db: AsyncSession = Depends(get_db)
):
    db_book = book_crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    
    # If ISBN is being updated, check it doesn't conflict
    if book.isbn and book.isbn != db_book.isbn:
        existing_book = book_crud.get_book_by_isbn(db, isbn=book.isbn)
        if existing_book:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Book with ISBN {book.isbn} already exists"
            )
    
    return book_crud.update_book(db=db, book_id=book_id, book=book)


@router.delete("/{book_id}", response_model=BookResponse)
def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db)
):
    db_book = book_crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book_crud.delete_book(db=db, book_id=book_id)