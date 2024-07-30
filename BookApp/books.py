from fastapi import FastAPI, Body


app = FastAPI()


BOOKS = [
    {"title": "Harry Potter", "author": "JK", "category": "fantasy"},
    {"title": "Harry Potter2", "author": "JK", "category": "fantasy"},
    {"title": "Game of Thrones", "author": "Geoge RR Martin", "category": "adventure"},
    {"title": "The Loard of The  Ring", "author": "John Ronald Reuel Tolkien", "category": "adventure"}
]


@app.get("/")
async def index():
    return {"message": "Welcome to book store"}


@app.get("/books")
async def get_all_books():
    return BOOKS


# dynamic parameter
@app.get("/books/{book_title}")
async def get_book(book_title):
    for book in BOOKS:
        
        if book["title"].casefold() == book_title.casefold():
            return book


# query parameter
@app.get("/query_book")
async def query_book(title: str='', author: str='', category: str=''):
    
    queried_books = []
    
    for book in BOOKS:
        
        matched_title = book["title"].casefold() == title.casefold()
        matched_author = book["author"].casefold() == author.casefold()
        matched_category = book["category"].casefold() == category.casefold()
        
        if any([matched_title, matched_author, matched_category]):
            queried_books.append(book)
            
    return queried_books
        
        
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    
    
@app.put("/books/update_book")
async def update_book(updated=Body()):
    
    for i, book in enumerate(BOOKS):
        
        if book["title"].casefold() == updated["title"].casefold():
            
            BOOKS[i] = updated            
            
            
@app.delete("/books/delete_book/{title}")
async def delete_book(title):
    
    for i, book in enumerate(BOOKS):
            
        if book["title"].casefold() == title.casefold():
            
            BOOKS.pop(i)
