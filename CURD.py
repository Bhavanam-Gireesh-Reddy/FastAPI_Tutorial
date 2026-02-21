from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic import BaseModel

books = [
    {
        "id" : 1, 
        "title" : "The Alchemist", 
        "author" : "Paulo Coelho", 
        "publish_date" : "1988-01-01"
    },
    {
        "id" : 2, 
        "title" : "The God of Small Things", 
        "author" : "Arundhati Roy", 
        "publish_date" : "1997-04-04"
    },
    {
        "id" : 3, 
        "title" : "The White Tiger", 
        "author" : "Aravind Adiga", 
        "publish_date" : "2008-01-01"
    },
    {
        "id" : 4, 
        "title" : "The Palace of Illusions", 
        "author" : "Chitra Banerjee Divakaruni", 
        "publish_date" : "2008-02-12"
    },
]

app = FastAPI()

@app.get("/books")
def read_all_books():
    return books

@app.get("/books/{book_id}")
def read_book(book_id : int):
    for book in books:
        if book.get("id") == book_id: # book[id] == book_id
            return book
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Book Not Found") # or we can also write normal return statement as Book Not Found.

class Book(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str

@app.post("/books")
def create_book(book:Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book

class BookUpdate(BaseModel):
    title: str
    author: str
    publish_date: str

@app.put("/books/{book_id}")
def update_book(book_id: int, book_update:BookUpdate):
    new_book = book_update.model_dump()
    for book in books:
        if book.get("id") == book_id:
            book.update(new_book)
            return book
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Book Not Found")

@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for book in books:
        if book.get("id") == book_id:
            books.remove(book)
            return {"Message" : "Book Deleted Successfully"}
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Book Not Found")     