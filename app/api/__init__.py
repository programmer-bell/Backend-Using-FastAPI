from fastapi import APIRouter
from .routes import book, members, loans

api_router = APIRouter()

api_router.include_router(book.router)
api_router.include_router(members.router)
api_router.include_router(loans.router)

# Export the router so it can be imported from app.api
__all__ = ['api_router']