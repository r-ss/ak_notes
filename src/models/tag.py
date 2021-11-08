from typing import Optional, List

import mongoengine as mongoengine
from pydantic import BaseModel


class Tag(mongoengine.Document):
    numerical_id = mongoengine.SequenceField(unique=True)
    name = mongoengine.StringField(max_length=32)


class TagBM(BaseModel):
    numerical_id: Optional[int]
    name: str


class TagsBM(BaseModel):
    __root__: List[TagBM]    # __root__