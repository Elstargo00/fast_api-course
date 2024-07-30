from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Todos
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from pydantic import BaseModel, Field
from .auth import get_current_user

router = APIRouter(tags=["Todo"])


def get_db():
    
    db = SessionLocal()
    try:
        yield db
    
    finally:
        db.close()
        


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt = 0, lt = 6)
    complete: bool
    
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Meditation",
                "description": "Meditate 45 mins everyday for the better life",
                "priority": 5,
                "complete": False 
            }
        }
    }

        
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Authentication failed"
        )
        
    return db.query(Todos).filter(Todos.owner_id==user.get("id")).all()


@router.get("/todos/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Authentication failed"
        )
    
    todo_item = db.query(Todos).filter(Todos.id==todo_id)\
        .filter(Todos.owner_id==user.get("id")).first()
    
    
    if not todo_item:
        raise HTTPException(
            status_code = 404,
            detail = "Todo not found."
        )
        
    return todo_item


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest
):
    
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Authentication failed"
        )
        
    todo_item = Todos(**todo_request.model_dump(), owner_id=user.get("id"))
    
    db.add(todo_item)
    db.commit()
    
    
    
    
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    user: user_dependency,
    db: db_dependency,
    todo_request: TodoRequest,
    todo_id: int = Path(gt=0)
):
    
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Authentication failed"
        )
    
    
    todo_item = db.query(Todos).filter(Todos.id==todo_id)\
        .filter(Todos.owner_id==user.get("id")).first()
    
    if not todo_item:
        raise HTTPException(
            status_code = 404,
            detail = "Todo not found."
        )
        
    todo_item.title = todo_request.title
    todo_item.description = todo_request.description
    todo_item.priority = todo_request.priority
    todo_item.complete = todo_request.complete
    
    db.add(todo_item)
    db.commit()
    
    
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    user: user_dependency,
    db: db_dependency,
    todo_id: int = Path(gt=0)
):
    
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Authentication failed"
        )
    
    todo_item = db.query(Todos).filter(Todos.id==todo_id)\
        .filter(Todos.owner_id==user.get("id")).first()
    
    if not todo_item:
        raise HTTPException(
            status_code = 404,
            detail = "Todo not found."
        )
        
    db.delete(todo_item)
    db.commit()
 