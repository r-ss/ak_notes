from typing import Optional, List

import mongoengine as mongoengine
from pydantic import BaseModel


class Category(mongoengine.Document):
    """ Represents Note Category. Like Default / Work / Personal etc """

    numerical_id = mongoengine.SequenceField(unique=True)
    name = mongoengine.StringField(max_length=32)

    def choose_default():
        # When note created, default category will be choosed for it and can be changed later
        return Category.objects.first()


class CategoryBM(BaseModel):
    numerical_id: Optional[int]
    name: Optional[str]


class CategoriesBM(BaseModel):
    __root__: List[CategoryBM]  # __root__
