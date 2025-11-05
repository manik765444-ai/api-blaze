# main.py

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Define a data model for the items
class Item(BaseModel):
    """Item data model."""
    id: int
    name: str
    description: Optional[str] = None
    price: float

# In-memory item database
items_db = [
    Item(id=1, name="Item 1", description="This is item 1", price=10.99),
    Item(id=2, name="Item 2", description="This is item 2", price=9.99),
]

# Read all items
@app.get("/items/", tags=["Items"], response_model=list[Item])
async def read_all_items():
    """
    Read all items.

    Returns:
        list[Item]: A list of all items.
    """
    return items_db

# Read item by ID
@app.get("/items/{item_id}", tags=["Items"], response_model=Item)
async def read_item(item_id: int):
    """
    Read item by ID.

    Args:
        item_id (int): The ID of the item to read.

    Returns:
        Item: The item with the given ID.
    """
    item = next((item for item in items_db if item.id == item_id), None)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item

# Create a new item
@app.post("/items/", tags=["Items"], response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    """
    Create a new item.

    Args:
        item (Item): The item to create.

    Returns:
        Item: The created item.
    """
    existing_item = next((existing_item for existing_item in items_db if existing_item.id == item.id), None)
    if existing_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item with this ID already exists")
    items_db.append(item)
    return item

# Update an existing item
@app.put("/items/{item_id}", tags=["Items"], response_model=Item)
async def update_item(item_id: int, item: Item):
    """
    Update an existing item.

    Args:
        item_id (int): The ID of the item to update.
        item (Item): The updated item data.

    Returns:
        Item: The updated item.
    """
    existing_item = next((existing_item for existing_item in items_db if existing_item.id == item_id), None)
    if not existing_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    existing_item.name = item.name
    existing_item.description = item.description
    existing_item.price = item.price
    return existing_item

# Delete an item
@app.delete("/items/{item_id}", tags=["Items"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """
    Delete an item.

    Args:
        item_id (int): The ID of the item to delete.
    """
    existing_item = next((existing_item for existing_item in items_db if existing_item.id == item_id), None)
    if not existing_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    items_db.remove(existing_item)
```

```python
# run.py
from main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)