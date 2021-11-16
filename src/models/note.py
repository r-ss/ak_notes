from typing import Optional, List
import datetime
import mongoengine as mongoengine

# import mongoengine_goodjson as gj # to follow linked objects on json output

from uuid import uuid4

from pydantic import BaseModel, constr

from models.user import UserBM
from models.category import CategoryBM

from config import config

import json


class Note(mongoengine.Document):
    """ Represents short text Note
        Main fields here are titile and body
        Note shoud have single category Like Default / Work / Personal etc
        Category can be changed after note creation
        Note can have multiple files assotiated with it
        Note can have multiple tags and can be listed by specific tag
        Note must have single owner as User model

        Note can be deleted
        TODO - remove assotiated with note files on deletion
    """

    numerical_id = mongoengine.SequenceField(unique=True)
    uuid = mongoengine.fields.UUIDField(binary=False, default=uuid4, required=True)
    created = mongoengine.DateTimeField(default=datetime.datetime.utcnow())
    modified = mongoengine.DateTimeField(default=datetime.datetime.utcnow())
    title = mongoengine.StringField(max_length=50)
    body = mongoengine.StringField(required=True)
    owner = mongoengine.ReferenceField('User', required=True)
    category = mongoengine.ReferenceField('Category', required=True)
    tags = mongoengine.ListField(mongoengine.StringField())

    @property
    def shortbody(self) -> str:
        return self.body[0:64]

    meta = {'ordering': ['-id']}

    def to_custom_json(self) -> str:
        data = json.loads(self.to_json())
        data['owner'] = json.loads(self.owner.to_json())
        data['category'] = json.loads(self.category.to_json())
        data['created'] = self.created.strftime(config.DATETIME_FORMAT_TECHNICAL)
        data['modified'] = self.modified.strftime(config.DATETIME_FORMAT_TECHNICAL)
        return json.dumps(data)


# Base model frame
class NoteBM(BaseModel):
    numerical_id: Optional[int]
    uuid: Optional[str]
    created: Optional[datetime.datetime]
    modified: Optional[datetime.datetime]
    title: constr(max_length=50)
    body: str


# Used on json output
class NoteExtendedBM(NoteBM):
    owner: Optional[UserBM]
    # files: Optional[list]
    category: Optional[CategoryBM]
    tags: Optional[List[str]]


# Usen upon note update - added Optional fields
class NoteEditBM(NoteBM):
    title: Optional[constr(max_length=50)]
    body: Optional[str]
    tags: Optional[list]


class NotesBM(BaseModel):
    __root__: List[NoteBM]  # __root__


class NotesExtendedBM(BaseModel):
    __root__: List[NoteExtendedBM]  # __root__
