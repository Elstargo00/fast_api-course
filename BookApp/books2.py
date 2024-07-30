from fastapi import FastAPI, Path, Query, HTTPException


from pydantic import BaseModel, Field
from typing import Optional

from starlette import status

app = FastAPI()

class Book():
    
    def __init__(self, id, title, author, description, rating, published_date=None):
        
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        
        
        
class BookRequest(BaseModel):
    
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: Optional[int] = Field(gt=1999, lt=2031, description="Year of publish", default=None)
    
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Harry Potter",
                "author": "JK",
                "description": "Fantasy magic",
                "rating": 5,
                "published_date": 2012
            }
        }
    }
    
        
        

BOOKS = [
    Book(1, "Computer Science Pro", "Roby", "A very nice book", 5, 2012),
    Book(2, "Be fast with FastAPI", "Roby", "A great book", 2, 2018),
    Book(3, "Confused billionare", "Jest", "An ultimate book for getting rich in your timeline", 5, 2024),
    Book(4, "Dogdag", "Dagdog", "Noob book for noob people", 1, 2025)

    
]



@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    
    queried_books = []
    
    for book in BOOKS:
        
        if book.rating == book_rating:
            
            queried_books.append(book)
    
    if not queried_books:
        raise HTTPException(
            status_code = 404,
            detail = {"message": "Item not found"}
        )
        
    return queried_books




@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    
    for book in BOOKS:
        
        if book.id == book_id:
            return book
        
    raise HTTPException(
        status_code = 404,
        detail = {"message": "Item not found"},
    )



@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    
    book_changed = False
    
    for i, book in enumerate(BOOKS):
        
        if book.id == book_id:
            BOOKS.pop(i)
            book_changed = True
            
    if not book_changed:
        raise HTTPException(
            status_code = 404,
            detail = {"message": "Item not found"},
        )



def find_book_id(book: Book):
    
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    
    return book



@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    new_book = find_book_id(new_book)
    BOOKS.append(new_book)
    
    
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(updating_book: BookRequest):
    
    book_changed = False
    
    for i, book in enumerate(BOOKS):
        
        if book.id == updating_book.id:
            BOOKS[i] = updating_book
            book_changed = True
            
    if not book_changed:
        raise HTTPException(
            status_code = 404,
            detail = {"message": "Item not found"},
        )
            
            
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    
    queried_books = []
    
    for book in BOOKS:
        
        if book.published_date == published_date:
            
            queried_books.append(book)
            
            
    if not queried_books:
        raise HTTPException(
            status_code = 404,
            detail = {"message": "Item not found"}
        )
        
    return queried_books