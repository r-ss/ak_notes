from datetime import datetime
from typing import Optional, List
from uuid import uuid4

import mongoengine as mongoengine
from pydantic import BaseModel, UUID4, constr
from pydantic.color import Color

from models.user import User
from models.category import Category
from models.note import Note


class Tag(mongoengine.Document):
    """ Represents Tag attached to Note

      ┌───────────────────────────────────┐
      │ Place in app's dataflow:          │
      │                         .-> File  │
      │ User -> Category -> Note -> Tag   │
      │                             ^^^   │
      └───────────────────────────────────┘

        parent: Note
        childrens: None
    """

    uuid = mongoengine.UUIDField(binary=False, default=uuid4, required=True, unique=True)
    created = mongoengine.DateTimeField(default=datetime.utcnow())
    name = mongoengine.StringField(max_length=32)
    color = mongoengine.StringField(max_length=256)

    @property
    def parent(self) -> Note:
        return Note.objects.filter(files__in=[self.uuid])[0]

    @property
    def owner(self) -> User:
        db_note = Note.objects.filter(files__in=[self.uuid])[0]
        db_category = Category.objects.filter(notes__in=[db_note.uuid])[0]
        db_user = User.objects.filter(categories__in=[db_category.uuid])[0]
        return db_user

    meta = {'ordering': ['-id']}  # Descending Order


class TagBM(BaseModel):
    uuid: Optional[UUID4]
    created: Optional[datetime]
    name: constr(max_length=32)
    color: Optional[Color] = Color('green')

    class Config:
        orm_mode = True


class TagsBM(BaseModel):
    __root__: List[TagBM]  # __root__

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]

    class Config:
        orm_mode = True


class TagEditBM(BaseModel):
    uuid: Optional[UUID4]
    name: Optional[constr(max_length=32)]
    color: Optional[Color]

    class Config:
        orm_mode = True
