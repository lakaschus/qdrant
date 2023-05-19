from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from uvicorn import run

# Define your data model
class Item(BaseModel):
    name: str
    description: str
    price: float

# Initialize the FastAPI app
app = FastAPI()

# Some dummy data
items = [
    {"name": "Item 1", "description": "This is an item", "price": 49.99},
    {"name": "Item 2", "description": "This is another item", "price": 29.99},
]

# Define an endpoint that returns the dummy data
@app.get("/items", response_model=List[Item])
async def read_items():
    return items

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, reload=True)