from datetime import datetime
import mongoengine as mongoengine

from pydantic import BaseModel
from typing import Optional

from fastapi import Form

from uuid import uuid4

class User(mongoengine.Document):
    uuid = mongoengine.fields.UUIDField(binary=False, default=uuid4, required=True)
    username = mongoengine.StringField(required=True, unique=True)
    # email = mongoengine.EmailField(required=True, unique=True)
    userhash = mongoengine.StringField(required=True, max_length=200)
    created = mongoengine.DateTimeField(default=datetime.utcnow())
    last_login = mongoengine.DateTimeField()
    is_superadmin = mongoengine.BooleanField(default=False)


class UserBM(BaseModel):
    uuid: Optional[str]
    username: str
    is_superadmin: Optional[bool] = False
    # userhash: Optional[str]

class UserRegBM(UserBM): # used upon user registeration
    password: Optional[str] 


class UserTokenBM(BaseModel): # used in token_required 
    username: str
    uuid: str
    is_superadmin: bool
    expires: str

class UserLoginFormBM(BaseModel): # used upon login
    username: str = Form(...)
    password: str = Form(...)
