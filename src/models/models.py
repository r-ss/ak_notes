from datetime import datetime
import mongoengine as mongoengine

# заметка имеет поля заголовок, тело (markdown), теги (список), owner, id (uuid), category_id, shortbody (для списка), files

class User(mongoengine.Document):
    username = mongoengine.StringField(required=True, unique=True)
    email = mongoengine.EmailField(required=True, unique=True)
    userhash = mongoengine.StringField(required=True, max_length=200, exclude_to_json=True)
    # is_superadmin = mongoengine.BooleanField(default=False)
    # lastactive = mongoengine.DateTimeField(default=datetime.utcnow())

class Category(mongoengine.Document):
    numerical_id = mongoengine.SequenceField(unique=True)
    name = mongoengine.StringField(max_length=32)

class Tag(mongoengine.Document):
    numerical_id = mongoengine.SequenceField(unique=True)
    name = mongoengine.StringField(max_length=32)

class Note(mongoengine.Document):
    numerical_id = mongoengine.SequenceField(unique=True)
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
