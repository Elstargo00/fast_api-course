from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from models import Todos, Users
from database import SessionLocal
from sqlalchemy.orm import Session
from typing import Annotated, Optional
from pydantic import BaseModel, Field
from .auth import get_current_user
# from passlib.context import CryptContext
from .auth import bcrypt_context

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


def get_db():
    
    db = SessionLocal()
    try:
        yield db
    
    finally:
        db.close()
        


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]





class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str
    new_password_confirm: str
    
    

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency):
    
    if not user:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "You're not allowed"
        )
               
    return user


@router.put("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    user: user_dependency,
    db: db_dependency,
    form_data: Annotated[ChangePasswordRequest, Depends()],
):
    
    if not user:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "You're not allowed"
        )
        
    user_item = db.query(Users).filter(Users.id==user.get("id")).first()
        
    if not bcrypt_context.verify(form_data.old_password, user_item.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Error on password change"
        )
        
    if form_data.new_password == form_data.new_password_confirm:
        user_item.hashed_password = bcrypt_context.hash(form_data.new_password)


    db.add(user_item)
    db.commit()
    
    
