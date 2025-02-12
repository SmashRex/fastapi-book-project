from fastapi import APIRouter

from api.routes import books_router

api_router = APIRouter()
api_router.include_router(books_router, prefix="/books", tags=["Books"])
