from typing import Optional, List

from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from config import Config

import mongoengine as mongoengine


# from models.models import Tag

from info import Info


# from fastapi_utils.inferring_router import InferringRouter

from views.tags import router as tags_router
from views.files import router as files_router



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



app.include_router(tags_router)
app.include_router(files_router)