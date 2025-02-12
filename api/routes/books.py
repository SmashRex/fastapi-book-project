from typing import OrderedDict
from collections import OrderedDict as OrderedDictType

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api.db.schemas import Book, Genre, InMemoryDB

router = APIRouter()

db = InMemoryDB()
db.books = OrderedDictType({  # Preserve order in the dictionary
    1: Book(
        id=1,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        publication_year=1937,
        genre=Genre.SCI_FI,
    ),
    2: Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        publication_year=1954,
        genre=Genre.FANTASY,
    ),
    3: Book(
        id=3,
        title="The Return of the King",
        author="J.R.R. Tolkien",
        publication_year=1955,
        genre=Genre.FANTASY,
    ),
})


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    db.add_book(book)
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content=book.model_dump()
    )


@router.get("/", response_model=OrderedDict[int, Book], status_code=status.HTTP_200_OK)
async def get_books() -> OrderedDict[int, Book]:
    return db.get_books()  

#geting the book by id
@router.get("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int):
    if book_id not in db.books:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "Book not found"})

    return JSONResponse(status_code=status.HTTP_200_OK, content=db.books[book_id].model_dump())


@router.put("/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: int, book: Book):
    updated_book = db.update_book(book_id, book)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=updated_book.model_dump(),
    )


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int):
    db.delete_book(book_id)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
