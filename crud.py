from fastapi import FastAPI,status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel  




books = [
    {"id": 1, 
     "title": "Book One", 
     "author": "Author One",
     "published_year": "14-02-2020"},

     {"id": 2,
     "title": "Book Two",
     "author": "Author Two",
     "published_year": "15-03-2021"},

    {"id": 3,
     "title": "Book Three",
     "author": "Author Three",
     "published_year": "16-04-2022"},

     {"id": 4,
     "title": "Book Four",
     "author": "Author Four",
     "published_year": "17-05-2023" },
]

app = FastAPI()

@app.get("/books")
def get_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

class Book(BaseModel):
    id: int
    title: str
    author: str
    published_year: str

@app.post("/book")
def create_book(book: Book):
   new_book = book.model_dump()
   books.append(new_book)
   return new_book


class UpdateBook(BaseModel):
    title: str
    author: str
    published_year: str

@app.put("/book/{book_id}")
def update_book(book_id: int, updated_book: UpdateBook):
    for book in books:
        if book["id"] == book_id:
            book["title"] = updated_book.title
            book["author"] = updated_book.author
            book["published_year"] = updated_book.published_year
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/book/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")