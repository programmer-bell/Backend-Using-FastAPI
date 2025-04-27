# This is the dependencies
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import book as book_crud
from app.crud import member as member_crud
from app.crud import loan as loan_crud


async def validate_book_exists(book_id: int, db: AsyncSession):
    book = await book_crud.get_book(db, book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {book_id} not found"
        )
    return book


async def validate_member_exists(member_id: int, db: AsyncSession):
    member = await member_crud.get_member(db, member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with ID {member_id} not found"
        )
    return member


async def validate_loan_exists(loan_id: int, db: AsyncSession):
    loan = await loan_crud.get_loan(db, loan_id)
    if not loan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Loan with ID {loan_id} not found"
        )
    return loan