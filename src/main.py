from typing import Optional, List

from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from config import Config

import mongoengine as mongoengine


from models.models import Tag

from info import Info



class TagBM(BaseModel):
    numerical_id: Optional[int]
    name: str

class TagsBM(BaseModel):
    __root__: List[TagBM]    # __root__



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

    tags = TagsBM.parse_raw(db_tags.to_json())
    return tags

@app.get("/tags/{numerical_id}")
def get_tag(numerical_id: int):

    try:
        db_tag = Tag.objects.get(numerical_id = numerical_id)
    except Tag.DoesNotExist:
        return JSONResponse(
            status_code = status.HTTP_404_NOT_FOUND,
            content = {'message': 'Tag does not found'}
        )

    db_tag = Tag.objects.get(numerical_id = numerical_id)
    tag = TagBM.parse_raw(db_tag.to_json())
    return tag


@app.post("/tags", status_code=status.HTTP_201_CREATED)
def create_tag(tag: TagBM):
    db_tag = Tag(name = tag.name).save()
    tag = TagBM.parse_raw(db_tag.to_json())
    return tag

@app.put("/tags/{numerical_id}")
def update_tag(numerical_id: int, tag: TagBM):
    db_tag = Tag.objects.get(numerical_id = numerical_id)
    db_tag.name = tag.name
    db_tag.save()
    tag = TagBM.parse_raw(db_tag.to_json())
    return tag


@app.delete("/tags/{numerical_id}", status_code=status.HTTP_204_NO_CONTENT)
def dels_tag(numerical_id: int):

    db_tag = Tag.objects.get(numerical_id = numerical_id)
    tag = TagBM.parse_raw(db_tag.to_json())

    db_tag.delete()
    return {'deteted tag': tag}