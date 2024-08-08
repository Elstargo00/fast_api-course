from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from fastapi.testclient import TestClient
from ..main import app
import pytest
from ..models import Todos, Users
from ..routers.auth import bcrypt_context




SQLALCHEMY_DATABASE = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE,
    connect_args = {"check_same_thread": False},
    poolclass = StaticPool
)


TestingSessionLocal = sessionmaker(
    autocommit = False,
    autoflush = False,
    bind = engine
)




Base.metadata.create_all(bind=engine)




def override_get_db():
    
    db = TestingSessionLocal()
    
    try:
        yield db
        
    finally:
        db.close()
        


def override_get_current_user():
    
    return {"username": "mirio00", "id": 1, "user_role": "admin"}



client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn to code!",
        description = "Need to learn everyday!",
        priority = 5,
        complete = False,
        owner_id = 1,
    )

    db = TestingSessionLocal() 
    db.add(todo)
    db.commit()
    
    yield todo
    
    
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()




@pytest.fixture
def test_user():
    
    user = Users(
        username = "mirio00",
        email = "mirio@example.com",
        first_name = "Mirio",
        last_name = "Togata",
        hashed_password = bcrypt_context.hash("mirio123"),
        role = "admin",
        phone_number = "1111111"    
    )
    
    db = TestingSessionLocal()
    
    db.add(user)
    db.commit()
    
    yield user
    
    with engine.connect() as connection:
        
        connection.execute(text("DELETE FROM users;"))
        connection.commit()