from typing import Optional, List

import mongoengine as mongoengine
from pydantic import BaseModel


class Category(mongoengine.Document):
    numerical_id = mongoengine.SequenceField(unique=True)
    name = mongoengine.StringField(max_length=32)


class CategoryBM(BaseModel):
    numerical_id: Optional[int]
    name: str


class CategoriesBM(BaseModel):
    __root__: List[CategoryBM]    # __root__