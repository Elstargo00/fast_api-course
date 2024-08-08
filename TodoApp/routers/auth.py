from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..models import Users
from passlib.context import CryptContext
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

from datetime import timedelta, datetime, timezone

router = APIRouter(
    prefix = "/auth",
    tags = ["Auth"]
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")



SECRET_KEY = "8ea1241d88d663c7bac6d7e07dc7d7391d612bf2c49f7df948e64c32bd148a66"
ALGORITHM = "HS256"


def get_db():
    
    db = SessionLocal()
    
    try:
        yield db
        
    finally:
        db.close()
        
        
        
def authenticate_user(username: str, password: str, db):
    
    user = db.query(Users).filter(Users.username == username).first()
    
    if not user:
        return False
        
    if not bcrypt_context.verify(password, user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Could not validate user."
        )
        
    return user


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM) 
    
    

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        
        if username is None or user_id is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Could not validate user."
            )
            
        return {"username": username, "id": user_id, "user_role": user_role}
    
    except JWTError:
        
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Could not validate user."
        )
    


db_dependency = Annotated[Session ,Depends(get_db)]
    


class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

class Token(BaseModel):
    access_token: str
    token_type: str 
    

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    
    user_input = create_user_request.model_dump()
    user_input["hashed_password"] = bcrypt_context.hash(user_input["password"])
    user_input.pop("password")
    
    user_item = Users(**user_input)
    
    if not user_item:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "User detail not found"
        )
    
    db.add(user_item)
    db.commit()
    

@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: db_dependency
    ):
    
    user = authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(
            status_code = 404,
            detail = "User not found."
        )
    

    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    
    return {"access_token": token, "token_type": "bearer"}



