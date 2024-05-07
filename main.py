from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# Instanciar nuestra API
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}


# /items/1?query={value}
# /items/1?query=Santiago
@app.get("/items/{id}")
def read_item(id: int, query: Union[str, None] = None):
    return {"id": id, "query": query}

@app.get("/items")
def read_item(item: Item):
    return item

#Response
# {
#     "id": 1,
#     "query": "Santiago"
# }