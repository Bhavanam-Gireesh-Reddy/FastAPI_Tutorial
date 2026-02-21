from fastapi import FastAPI, Depends
from database import engine, get_db
import model
from sqlalchemy.orm import Session
from pydantic import BaseModel

app = FastAPI()

class Bookstore(BaseModel):
    id: int
    title: str
    author: str
    published_date: str

@app.post("/book")
def create_book(book: Bookstore, db: Session = Depends(get_db)):
    new_book = model.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@app.get("/books")
def read_all_books(db: Session = Depends(get_db)):
    books = db.query(model.Book).all()
    return books