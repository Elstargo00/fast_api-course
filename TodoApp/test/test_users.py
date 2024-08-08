from ..routers.users import get_db, get_current_user, ChangePasswordRequest
from fastapi import status
from ..models import Users


from .utils import (override_get_db, override_get_current_user, 
                    client, TestingSessionLocal, app, test_todo,
                    test_user)

import json


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user






def test_return_user(test_user):
    
    response = client.get("/users")
    
    assert response.status_code == status.HTTP_200_OK
    
    assert response.json()["username"] == "mirio00"
    assert response.json()["email"] == "mirio@example.com"
    assert response.json()["first_name"] == "Mirio"
    assert response.json()["last_name"] == "Togata"
    assert response.json()["role"] == "admin"
    assert response.json()["phone_number"] == "1111111"



def test_change_password_success(test_user):
    
    request_data = {
        "old_password": "mirio123",
        "new_password": "testpass",
        "new_password_confirm": "testpass"
    }

    
    response = client.put("/users/change_password", json=request_data)
    
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    
    
def test_change_password_invalid_current_password(test_user):
    
    
    request_data = {
        "old_password": "wrongpassword",
        "new_password": "testpass",
        "new_password_confirm": "testpass"
    }
    
    response = client.put("/users/change_password", json=request_data)
    
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"detail": "Error on password change."}
    
    
    
    
def test_change_phone_number_sccess(test_user):
    
    response = client.put("/users/update_phone_number/2222222")
    
    assert response.status_code == status.HTTP_204_NO_CONTENT