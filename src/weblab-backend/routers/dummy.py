import secrets
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer
from pydantic import BaseModel

router = APIRouter(
    prefix="/dummy",
    tags=["dummy"],
    responses={404: {"description": "Not found"}}
)


class Data(BaseModel):
    data: str
    
# Basic Auth setup
basic_auth = HTTPBasic()

# Bearer Token setup
bearer_auth = HTTPBearer()

def get_current_user(authorization: str = Depends(bearer_auth)):
    token = authorization.credentials
    if token != "token":  # Replace with your actual logic to validate the token
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return {"username": "fastapi"}  # Return some user information here

def get_current_basic_user(credentials: Optional[HTTPBasicCredentials] = Depends(basic_auth)):
    correct_username = secrets.compare_digest("username", credentials.username)
    correct_password = secrets.compare_digest("password", credentials.password)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"username": credentials.username}

@router.get("/protected-bearer")
def protected_by_bearer(user = Depends(get_current_user)):
    return user

@router.get("/protected-basic")
def protected_by_basic(user = Depends(get_current_basic_user)):
    return user

@router.get("/")
async def get_data():
    return [{"username": "Rick"}, {"username": "Morty"}]

@router.post("/create")
def create_item(data: Data):
    # Logic to create a new item
    return {"status": "created", "data": data.data}

@router.put("/update/{item_id}")
def update_item(item_id: int, request: Request):
    data = request.json()  # Assuming the body is in JSON format
    # Logic to update an existing item with ID item_id
    return {"status": "updated", "item_id": item_id}

@router.delete("/delete/{item_id}")
def delete_item(item_id: int):
    # Logic to delete the item with ID item_id
    return {"status": "deleted", "item_id": item_id}

@router.patch("/update/{item_id}")
def patch_item(item_id: int, request: Request):
    data = request.json()  # Assuming the body is in JSON format
    # Logic to partially update the item with ID item_id
    return {"status": "partially updated", "item_id": item_id}
