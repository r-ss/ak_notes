from datetime import datetime
import mongoengine as mongoengine

class User(mongoengine.Document):
    username = mongoengine.StringField(required=True, unique=True)
    # email = mongoengine.EmailField(required=True, unique=True)
    userhash = mongoengine.StringField(required=True, max_length=200)
    created = mongoengine.DateTimeField(default=datetime.utcnow())