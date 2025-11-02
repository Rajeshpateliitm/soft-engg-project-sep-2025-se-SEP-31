from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import List, Optional

router = APIRouter()

# Sample user data
users_db = [
    {"id": 1, "username": "user1", "email": "user1@example.com", "full_name": "User One"},
    {"id": 2, "username": "user2", "email": "user2@example.com", "full_name": "User Two"},
]

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

@router.get("/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 10):
    return users_db[skip : skip + limit]

@router.get("/{user_id}", response_model=User)
async def read_user(user_id: int):
    if user_id < 1 or user_id > len(users_db):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return users_db[user_id - 1]

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    new_user = {
        "id": len(users_db) + 1,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
    }
    users_db.append(new_user)
    return new_user
