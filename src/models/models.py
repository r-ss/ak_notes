from datetime import datetime
import mongoengine as mongoengine

from uuid import uuid4

# заметка имеет поля заголовок, тело (markdown), теги (список), owner, id (uuid), category_id, shortbody (для списка), files

class Category(mongoengine.Document):
    numerical_id = mongoengine.SequenceField(unique=True)
    name = mongoengine.StringField(max_length=32)

class Note(mongoengine.Document):
    numerical_id = mongoengine.SequenceField(unique=True)
    uuid = mongoengine.fields.UUIDField(Binary=False, default=uuid4(), required=True)
    created = mongoengine.DateTimeField(default=datetime.utcnow())
    modified = mongoengine.DateTimeField(default=datetime.utcnow())
    title = mongoengine.StringField(max_length=50)
    body = mongoengine.StringField(required=True)
    owner = mongoengine.ReferenceField('User', required=True)
    files = mongoengine.ListField()
    category = mongoengine.ReferenceField('Category', required=True)
    tags = mongoengine.ListField()

    @property
    def shortbody(self):
        return self.body[0:64]
