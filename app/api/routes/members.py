from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.db import get_db
from app.schemas.member import MemberCreate, MemberUpdate, MemberResponse
from app.crud import member as member_crud
router = APIRouter(
    prefix="/members",
    tags=["members"],
)


@router.post("/", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(
    member: MemberCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new member in the library system.
    """
    # Check if member with same email already exists
    db_member = member_crud.get_member_by_email(db, email=member.email)
    if db_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Member with email {member.email} already exists"
        )
    return member_crud.create_member(db=db, member=member)


@router.get("/", response_model=List[MemberResponse])
def read_members(
    skip: int = 0,
    limit: int = 100,
    active: Optional[bool] = None,
    name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    members = member_crud.get_members(
        db, skip=skip, limit=limit, 
        active=active, name=name
    )
    return members


@router.get("/{member_id}", response_model=MemberResponse)
def read_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    db_member = member_crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    return db_member


@router.put("/{member_id}", response_model=MemberResponse)
def update_member(
    member_id: int,
    member: MemberUpdate,
    db: Session = Depends(get_db)
):
    db_member = member_crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    
    # If email is being updated, check it doesn't conflict
    if member.email and member.email != db_member.email:
        existing_member = member_crud.get_member_by_email(db, email=member.email)
        if existing_member:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Member with email {member.email} already exists"
            )
    
    return member_crud.update_member(db=db, member_id=member_id, member=member)


@router.delete("/{member_id}", response_model=MemberResponse)
def delete_member(
    member_id: int,
    db: Session = Depends(get_db)
):
    db_member = member_crud.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found"
        )
    return member_crud.delete_member(db=db, member_id=member_id)