from fastapi import FastAPI, HTTPException
from typing import List, Optional, Dict
from pydantic import BaseModel

app = FastAPI()


class Author(BaseModel):
    id: int
    name: str
    books: list


class Book(BaseModel):
    id: int
    title: str
    description: str
    author: Author


authors = [
    {
        "id": 1,
        "name": "Leo Tolstoy",
        "books": ["War and Peace"]
    },
    {
        "id": 2,
        "name": "George Orwell",
        "books": ["1984"]
    },
    {
        "id": 3,
        "name": "Fyodor Dostoevsky",
        "books": ["Crime and Punishment"]
    },
    {
        "id": 4,
        "name": "J.K. Rowling",
        "books": ["Harry Potter and the Sorcerer's Stone"]
    }
]

books = [
    {
        "id": 1,
        "title": "War and Peace",
        "description": "A novel about the life of Russian society during the Napoleonic wars.",
        "author": authors[0]
    },
    {
        "id": 2,
        "title": "1984",
        "description": "A dystopian novel by George Orwell about a totalitarian state.",
        "author": authors[1]

    },
    {
        "id": 3,
        "title": "Crime and Punishment",
        "description": "A novel by Fyodor Dostoevsky that explores moral dilemmas.",
        "author": authors[2]
    },
    {
        "id": 4,
        "title": "Harry Potter and the Sorcerer's Stone",
        "description": "The first book in the Harry Potter series, set in the magical world.",
        "author": authors[3]
    }
]


# @app.get("/books")
# async def get_books() -> List[Book]:
#     book_objects = []
#     for book in books:
#         book_objects.append(Book(id=book["id"], title=book["title"], description=book["description"]), author[''])
#
#     return book_objects

@app.get("/books")
async def get_books() -> List[Book]:
    return [Book(**book) for book in books]


@app.get("/books/{id}")
async def get_book(id: int) -> Book:
    for book in books:
        if book["id"] == id:
            return Book(**book)
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/search")
async def search(book_id: Optional[int] = None) -> Dict[str, Optional[Book]]:
    if book_id:
        for book in books:
            if book["id"] == book_id:
                return {"data": Book(**book)}
        raise HTTPException(status_code=404, detail="Book not found")
    else:
        return {"data": None}


@app.get("/authors")
async def get_authors() -> List[Author]:
    return [Author(**author) for author in authors]


@app.get("/authors/{id}")
async def get_author(id: int) -> Author:
    for author in authors:
        if author["id"] == id:
            return Author(**author)
    raise HTTPException(status_code=404, detail="Author not found")
