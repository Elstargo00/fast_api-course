from fastapi import FastAPI


app = FastAPI()


BOOKS = [
    {"title": "Harry Potter", "author": "JK", "category": "magic"},
    {"title": "Game of Thrones", "author": "Geoge RR Martin", "category": "adventure"},
]


@app.get("/")
async def index():
    return {"message": "Welcome to book store"}


@app.get("/books")
async def get_book():
    return BOOKS