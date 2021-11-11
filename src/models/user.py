from datetime import datetime
import mongoengine as mongoengine

from pydantic import BaseModel
from typing import Optional

from uuid import uuid4

class User(mongoengine.Document):
    uuid = mongoengine.fields.UUIDField(binary=False, default=uuid4(), required=True)
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

class UserRegBM(UserBM): # used upon user registeration and password change
    password: Optional[str] 

class UserTokenBM(BaseModel): # used in check token function in user_auth
    token: str

class UserTokenDataBM(BaseModel): # used in functions wrapped in token_required decorator
    username: str
    uuid: str
    expires: str