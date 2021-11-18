from datetime import datetime
import mongoengine as mongoengine

from pydantic import BaseModel, UUID4
from typing import Optional

from fastapi import Form

from uuid import uuid4


class User(mongoengine.Document):
    """ Represents User in database.

        Place in app's dataflow:
                                .-> Tag  
        User -> Category -> Note -> File
        ^^^^
        
        parent: None
        childrens: Category
    """

    uuid = mongoengine.fields.UUIDField(binary=False, default=uuid4, required=True)
    username = mongoengine.StringField(required=True, unique=True)
    # email = mongoengine.EmailField(required=True, unique=True)
    userhash = mongoengine.StringField(required=True, max_length=200)
    created = mongoengine.DateTimeField(default=datetime.utcnow())
    last_login = mongoengine.DateTimeField()
    is_superadmin = mongoengine.BooleanField(default=False)
    categories = mongoengine.ListField(mongoengine.UUIDField(binary=False))

    meta = {'ordering': ['-id']}  # Descending Order


class UserBM(BaseModel):
    uuid: Optional[UUID4]
    username: str
    is_superadmin: Optional[bool] = False

    class Config:
        orm_mode = True


class UserRegBM(UserBM):  # used upon user registeration
    password: Optional[str]


class UserTokenBM(BaseModel):  # used in token_required
    username: str
    uuid: str
    is_superadmin: bool
    expires: str


class UserLoginFormBM(BaseModel):  # used upon login
    username: str = Form(...)
    password: str = Form(...)
