from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    desc : str | None = None
    quantity: int


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.post("/create/{item_id}")
async def create_something(item_id: int, itemDetails: Item):
    print(itemDetails)
    return {"item_id": item_id}