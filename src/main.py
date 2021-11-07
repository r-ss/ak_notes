from typing import Optional

from fastapi import FastAPI
from fastapi.testclient import TestClient

from pydantic import BaseModel

from config import Config

import mongoengine as mongoengine


from models.models import Tag

from info import Info


class TagBM(BaseModel):
    name: str

mg = mongoengine.connect(host=Config.DBHOST)


app = FastAPI()
testclient = TestClient(app)

class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/info")
def info():
    return Info().get()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):

    t = Tag.objects.all().count()
    print('tags', t)

    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}



@app.get("/tags")
def get_tags():
    db_tags = Tag.objects.all()
    return {"tags": db_tags.to_json()}


@app.post("/tag")
def create_tag(tag: TagBM):
    db_tag = Tag(name = tag.name).save()
    return {"tag": db_tag.name}