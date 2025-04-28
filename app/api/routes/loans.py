from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from app.database.db import get_db
from app.schemas.loan import LoanCreate, LoanUpdate, LoanResponse, LoanDetailResponse
from app.crud import loan as loan_crud
from app.crud import book as book_crud
from app.crud import member as member_crud

router = APIRouter(
    prefix="/loans",
    tags=["loans"],
)


@router.post("/", response_model=LoanResponse, status_code=status.HTTP_201_CREATED)
def create_loan(
    loan: LoanCreate,
    db: AsyncSession = Depends(get_db)
):

    book =  book_crud.get_book(db, book_id=loan.book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ID {loan.book_id} not found"
        )
    if not book.available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Book with ID {loan.book_id} is not available for loan"
        )
    member = member_crud.get_member(db, member_id=loan.member_id)
    if not member:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Member with ID {loan.member_id} not found"
        )
    if not member.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Member with ID {loan.member_id} is not active"
        )
    
    return loan_crud.create_loan(db=db, loan=loan)


@router.get("/", response_model=List[LoanDetailResponse])
def read_loans(
    skip: int = 0,
    limit: int = 100,
    member_id: Optional[int] = None,
    book_id: Optional[int] = None,
    is_returned: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    loans =  loan_crud.get_loans(
        db, skip=skip, limit=limit,
        member_id=member_id, book_id=book_id, 
        is_returned=is_returned
    )
    result = []
    for loan in loans:
        loan_dict = {
            "id": loan.id,
            "book_id": loan.book_id,
            "member_id": loan.member_id,
            "loan_date": loan.loan_date,
            "due_date": loan.due_date,
            "return_date": loan.return_date,
            "created_at": loan.created_at,
            "updated_at": loan.updated_at,
            "book_title": loan.book.title if loan.book else "Unknown Book",
            "member_name": f"{loan.member.first_name} {loan.member.last_name}" if loan.member else "Unknown Member"
        }
        result.append(loan_dict)
    
    return result


@router.get("/overdue", response_model=List[LoanDetailResponse])
def read_overdue_loans(
    current_date: Optional[date] = None,
    db: AsyncSession = Depends(get_db)
):
    if current_date is None:
        current_date = date.today()
        
    loans = loan_crud.get_overdue_loans(db, current_date=current_date)
    
    result = []
    for loan in loans:
        loan_dict = {
            "id": loan.id,
            "book_id": loan.book_id,
            "member_id": loan.member_id,
            "loan_date": loan.loan_date,
            "due_date": loan.due_date,
            "return_date": loan.return_date,
            "created_at": loan.created_at,
            "updated_at": loan.updated_at,
            "book_title": loan.book.title if loan.book else "Unknown Book",
            "member_name": f"{loan.member.first_name} {loan.member.last_name}" if loan.member else "Unknown Member"
        }
        result.append(loan_dict)
    
    return result


@router.get("/{loan_id}", response_model=LoanDetailResponse)
def read_loan(
    loan_id: int,
    db: AsyncSession = Depends(get_db)
):
    loan = loan_crud.get_loan(db, loan_id=loan_id)
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    
    return {
        "id": loan.id,
        "book_id": loan.book_id,
        "member_id": loan.member_id,
        "loan_date": loan.loan_date,
        "due_date": loan.due_date,
        "return_date": loan.return_date,
        "created_at": loan.created_at,
        "updated_at": loan.updated_at,
        "book_title": loan.book.title if loan.book else "Unknown Book",
        "member_name": f"{loan.member.first_name} {loan.member.last_name}" if loan.member else "Unknown Member"
    }


@router.put("/{loan_id}", response_model=LoanDetailResponse)
def update_loan(
    loan_id: int,
    loan_update: LoanUpdate,
    db: AsyncSession = Depends(get_db)
):
    loan =  loan_crud.get_loan(db, loan_id=loan_id)
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    
    updated_loan =  loan_crud.update_loan(db=db, loan_id=loan_id, loan_update=loan_update)
    return {
        "id": updated_loan.id,
        "book_id": updated_loan.book_id,
        "member_id": updated_loan.member_id,
        "loan_date": updated_loan.loan_date,
        "due_date": updated_loan.due_date,
        "return_date": updated_loan.return_date,
        "created_at": updated_loan.created_at,
        "updated_at": updated_loan.updated_at,
        "book_title": updated_loan.book.title if updated_loan.book else "Unknown Book",
        "member_name": f"{updated_loan.member.first_name} {updated_loan.member.last_name}" if updated_loan.member else "Unknown Member"
    }


@router.delete("/{loan_id}", response_model=LoanResponse)
def delete_loan(
    loan_id: int,
    db: AsyncSession = Depends(get_db)
):
    loan = loan_crud.get_loan(db, loan_id=loan_id)
    if loan is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Loan not found"
        )
    return loan_crud.delete_loan(db=db, loan_id=loan_id)

