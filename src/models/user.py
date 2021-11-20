from datetime import datetime
import mongoengine as mongoengine

from pydantic import BaseModel, constr, UUID4
from typing import Optional, List

from fastapi import Form

from uuid import uuid4


class User(mongoengine.Document):
    """ Represents User in database.

      ┌───────────────────────────────────┐
      │ Place in app's dataflow:          │
      │                         .-> Tag   │
      │ User -> Category -> Note -> File  │
      │ ^^^^                              │
      └───────────────────────────────────┘

        parent: None
        childrens: Category
    """

    uuid = mongoengine.UUIDField(binary=False, default=uuid4, required=True)
    username = mongoengine.StringField(required=True, unique=True, max_length=36)
    # email = mongoengine.EmailField(required=True, unique=True)
    userhash = mongoengine.StringField(required=True, max_length=200)
    created = mongoengine.DateTimeField(default=datetime.utcnow())
    last_login = mongoengine.DateTimeField()
    is_superadmin = mongoengine.BooleanField(default=False)
    categories = mongoengine.ListField(mongoengine.UUIDField(binary=False), default=[])

    meta = {'ordering': ['-id']}  # Descending Order


class UserBM(BaseModel):
    uuid: Optional[UUID4]
    username: constr(max_length=36)
    is_superadmin: Optional[bool] = False
    categories: Optional[List[UUID4]] = []

    class Config:
        orm_mode = True


class UserRegBM(UserBM):  # used upon user registeration
    password: Optional[str]


class UserTokenBM(BaseModel):  # used in token_required
    username: constr(max_length=36)
    uuid: UUID4
    is_superadmin: bool
    iat: constr(max_length=100)
    exp: constr(max_length=100)
    scope: constr(max_length=15)


class UserLoginFormBM(BaseModel):  # used upon login
    username: str = Form(...)
    password: str = Form(...)


class UsersBM(BaseModel):
    __root__: List[UserBM]  # __root__

    class Config:
        orm_mode = True
