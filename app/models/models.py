from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta
from app.database.db import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False)
    isbn = Column(String, unique=True, index=True)
    publication_year = Column(Integer)
    genre = Column(String)
    description = Column(String)
    available = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationship
    loans = relationship("Loan", back_populates="book")


class Member(Base):
    __tablename__ = "members"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String)
    address = Column(String)
    registration_date = Column(Date, default=datetime.utcnow)
    active = Column(Boolean, default=True)

    # Relationship
    loans = relationship("Loan", back_populates="member")


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    member_id = Column(Integer, ForeignKey("members.id"), nullable=False)
    loan_date = Column(Date, default=datetime.utcnow)
    due_date = Column(Date, default=lambda: datetime.utcnow() + timedelta(days=14))
    return_date = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    book = relationship("Book", back_populates="loans")
    member = relationship("Member", back_populates="loans")