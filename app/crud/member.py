from sqlalchemy import select, update, delete
from typing import Optional, List
from app.models.models import Member
from app.schemas.member import MemberCreate, MemberUpdate


def get_member(db, member_id: int):
    """Get a member by ID"""
    result = db.execute(select(Member).where(Member.id == member_id))
    return result.scalars().first()


def get_member_by_email(db, email: str):
    """Get a member by email"""
    result = db.execute(select(Member).where(Member.email == email))
    return result.scalars().first()


def get_members(
    db,
    skip: int = 0,
    limit: int = 100,
    active: Optional[bool] = None,
    name: Optional[str] = None
):
    """Get all members with optional filtering"""
    query = select(Member)
    
    # Apply filters if provided
    if active is not None:
        query = query.filter(Member.active == active)
    if name:
        query = query.filter(
            (Member.first_name.ilike(f"%{name}%")) | 
            (Member.last_name.ilike(f"%{name}%"))
        )

    query = query.offset(skip).limit(limit)
    result = db.execute(query)
    return result.scalars().all()


def create_member(db, member: MemberCreate):
    """Create a new member"""
    db_member = Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


def update_member(db, member_id: int, member: MemberUpdate):
    """Update a member"""
    # Filter out None values
    update_data = {k: v for k, v in member.model_dump().items() if v is not None}
    if not update_data:
        return get_member(db, member_id)
    
    db.execute(
        update(Member)
        .where(Member.id == member_id)
        .values(**update_data)
    )
    db.commit()
    return get_member(db, member_id)


def delete_member(db, member_id: int):
    """Delete a member"""
    member = get_member(db, member_id)
    if member:
        db.execute(delete(Member).where(Member.id == member_id))
        db.commit()
    return member