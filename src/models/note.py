from typing import Optional, List
import datetime
import mongoengine as mongoengine
# import mongoengine_goodjson as gj # to follow linked objects on json output

from uuid import uuid4

from pydantic import BaseModel, constr

from models.user import UserBM
from models.category import CategoryBM

import json
from bson import json_util

# заметка имеет поля заголовок, тело (markdown), теги (список), owner, id (uuid), category_id, shortbody (для списка), files

class Note(mongoengine.Document):
    numerical_id = mongoengine.SequenceField(unique=True)
    uuid = mongoengine.fields.UUIDField(binary=False, default=uuid4(), required=True)
    created = mongoengine.DateTimeField(default=datetime.datetime.utcnow())
    modified = mongoengine.DateTimeField(default=datetime.datetime.utcnow())
    title = mongoengine.StringField(max_length=50)
    body = mongoengine.StringField(required=True)
    owner = mongoengine.ReferenceField('User', required=True)
    files = mongoengine.ListField()
    category = mongoengine.ReferenceField('Category', required=True)
    tags = mongoengine.ListField()

    @property
    def shortbody(self) -> str:
        return self.body[0:64]

    meta = {
        'ordering': ['-id']
    }

    def to_custom_json(self) -> str:
        data = json.loads(self.to_json())      
        data['owner'] = json.loads(self.owner.to_json())
        data['category'] = json.loads(self.category.to_json())
        data['created'] = str(self.created)
        data['modified'] = str(self.modified)
        return json.dumps(data)




class NoteBM(BaseModel):
    numerical_id: Optional[int]
    uuid: Optional[str]
    created: Optional[datetime.datetime]
    modified: Optional[datetime.datetime]
    title: constr(max_length=50)
    body: str
    owner: Optional[UserBM]
    files: Optional[list]
    category: Optional[CategoryBM]
    tags: Optional[list]


class NotesBM(BaseModel):
    __root__: List[NoteBM]    # __root__