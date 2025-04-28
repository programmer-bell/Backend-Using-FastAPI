from sqlalchemy import select, update, delete, and_
from sqlalchemy.orm import joinedload
from typing import Optional, List
from datetime import date
from app.models.models import Loan, Book, Member
from app.schemas.loan import LoanCreate, LoanUpdate


def get_loan(db, loan_id: int):
    """Get a loan by ID"""
    result = db.execute(
        select(Loan)
        .options(joinedload(Loan.book), joinedload(Loan.member))
        .where(Loan.id == loan_id)
    )
    return result.scalars().first()


def get_loans(
    db,
    skip: int = 0,
    limit: int = 100,
    member_id: Optional[int] = None,
    book_id: Optional[int] = None,
    is_returned: Optional[bool] = None,
):
    """Get all loans with optional filtering"""
    query = select(Loan).options(joinedload(Loan.book), joinedload(Loan.member))
    
    # Apply filters if provided
    if member_id:
        query = query.filter(Loan.member_id == member_id)
    if book_id:
        query = query.filter(Loan.book_id == book_id)
    if is_returned is not None:
        if is_returned:
            query = query.filter(Loan.return_date.isnot(None))
        else:
            query = query.filter(Loan.return_date.is_(None))

    query = query.offset(skip).limit(limit)
    result = db.execute(query)
    return result.scalars().all()


def create_loan(db, loan: LoanCreate):
    """Create a new loan and update book availability"""
    # Create loan record
    db_loan = Loan(**loan.model_dump())
    
    # Update book availability
    db.execute(
        update(Book)
        .where(Book.id == loan.book_id)
        .values(available=False)
    )
    
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)
    return db_loan


def update_loan(db, loan_id: int, loan_update: LoanUpdate):
    """Update a loan and handle book return if applicable"""
    update_data = {k: v for k, v in loan_update.model_dump().items() if v is not None}
    
    # If returning a book, update the book's availability
    if "return_date" in update_data and update_data["return_date"] is not None:
        loan = get_loan(db, loan_id)
        if loan:
            db.execute(
                update(Book)
                .where(Book.id == loan.book_id)
                .values(available=True)
            )
    
    if update_data:
        db.execute(
            update(Loan)
            .where(Loan.id == loan_id)
            .values(**update_data)
        )
        db.commit()
    
    return get_loan(db, loan_id)


def delete_loan(db, loan_id: int):
    """Delete a loan"""
    loan = get_loan(db, loan_id)
    if loan:
        # If the loan is for a book that's not returned yet, make it available again
        if not loan.return_date:
            db.execute(
                update(Book)
                .where(Book.id == loan.book_id)
                .values(available=True)
            )
        
        db.execute(delete(Loan).where(Loan.id == loan_id))
        db.commit()
    
    return loan


def get_overdue_loans(db, current_date: date = None):
    """Get all overdue loans"""
    if current_date is None:
        current_date = date.today()
    
    query = (
        select(Loan)
        .options(joinedload(Loan.book), joinedload(Loan.member))
        .where(
            and_(
                Loan.due_date < current_date,
                Loan.return_date.is_(None)
            )
        )
    )
    
    result = db.execute(query)
    return result.scalars().all()
