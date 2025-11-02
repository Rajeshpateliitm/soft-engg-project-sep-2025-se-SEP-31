from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

router = APIRouter()

# Sample data
items_db = [
    {"id": 1, "name": "Item 1", "description": "First item"},
    {"id": 2, "name": "Item 2", "description": "Second item"},
]

class ItemCreate(BaseModel):
    name: str
    description: str = None

@router.get("/", response_model=List[dict])
async def read_items(skip: int = 0, limit: int = 10):
    return items_db[skip : skip + limit]

@router.get("/{item_id}", response_model=dict)
async def read_item(item_id: int):
    if item_id < 0 or item_id >= len(items_db):
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id - 1]

@router.post("/", response_model=dict, status_code=201)
async def create_item(item: ItemCreate):
    new_item = {
        "id": len(items_db) + 1,
        "name": item.name,
        "description": item.description,
    }
    items_db.append(new_item)
    return new_item
