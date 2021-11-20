from typing import Optional, List
import datetime
import mongoengine as mongoengine

from uuid import uuid4

from pydantic import BaseModel, constr, UUID4

from models.user import User
from models.category import Category

# from config import config


class Note(mongoengine.Document):
    """ Represents Note in database.

        Main fields here are titile and body
        Note created under single category Like Work / Personal etc
        Category can be changed after note creation
        Note can have multiple files assotiated with it
        Note can have multiple tags and can be listed by specific tag
        Note can be deleted
        TODO - remove assotiated with note files on deletion

      ┌───────────────────────────────────┐
      │ Place in app's dataflow:          │
      │                         .-> Tag   │
      │ User -> Category -> Note -> File  │
      │                     ^^^^          │
      └───────────────────────────────────┘

        parent: Category
        childrens: Tag, File
    """

    numerical_id = mongoengine.SequenceField(unique=True)
    uuid = mongoengine.UUIDField(binary=False, default=uuid4, required=True)
    created = mongoengine.DateTimeField(default=datetime.datetime.utcnow())
    modified = mongoengine.DateTimeField(default=datetime.datetime.utcnow())
    title = mongoengine.StringField(max_length=200)
    body = mongoengine.StringField(max_length=10000)
    tags = mongoengine.ListField(mongoengine.UUIDField(binary=False), default=[])
    files = mongoengine.ListField(mongoengine.UUIDField(binary=False), default=[])

    @property
    def shortbody(self) -> str:
        return self.body[0:64]

    @property
    def parent(self) -> Category:
        return Category.objects.filter(notes__in=[self.uuid])[0]

    @property
    def owner(self) -> User:
        return User.objects.filter(categories__in=[self.parent.uuid])[0]

    meta = {'ordering': ['-id']}  # Descending Order


class NoteBM(BaseModel):
    numerical_id: Optional[int]
    uuid: Optional[UUID4]
    created: Optional[datetime.datetime]
    modified: Optional[datetime.datetime]
    title: constr(max_length=200)
    body: constr(max_length=10000)
    tags: Optional[List[UUID4]]
    files: Optional[List[UUID4]]

    class Config:
        orm_mode = True


# Usen upon note update - added Optional fields
class NoteEditBM(NoteBM):
    uuid: UUID4
    title: Optional[constr(max_length=200)]
    body: Optional[constr(max_length=10000)]
    # tags: Optional[List[UUID4]]

    class Config:
        orm_mode = True


class NotesBM(BaseModel):
    __root__: List[NoteBM]  # __root__

    class Config:
        orm_mode = True
