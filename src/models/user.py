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
    is_superadmin = mongoengine.BooleanField(default=False)


class UserBM(BaseModel):
    uuid: Optional[str]
    username: str
    password: Optional[str] = None # used upon user registeration and password change
    is_superadmin: Optional[bool] = False
    # userhash: Optional[str]