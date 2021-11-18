from typing import Optional, List
import datetime
import mongoengine as mongoengine

# import mongoengine_goodjson as gj # to follow linked objects on json output

from uuid import uuid4

from pydantic import BaseModel, constr, UUID4

from models.user import UserBM
# from models.category import CategoryBM

from config import config


class Note(mongoengine.Document):
    """ Represents Note in database.

        Main fields here are titile and body
        Note shoud have single category Like Work / Personal etc
        Category can be changed after note creation
        Note can have multiple files assotiated with it
        Note can have multiple tags and can be listed by specific tag
        Note must have single owner as User model

        Note can be deleted
        TODO - remove assotiated with note files on deletion


        Place in app's dataflow:
                                .-> Tag  
        User -> Category -> Note -> File
                            ^^^^
        
        parent: Category
        childrens: Tag, File
    """

    numerical_id = mongoengine.SequenceField(unique=True)
    uuid = mongoengine.fields.UUIDField(binary=False, default=uuid4, required=True)
    created = mongoengine.DateTimeField(default=datetime.datetime.utcnow())
    modified = mongoengine.DateTimeField(default=datetime.datetime.utcnow())
    title = mongoengine.StringField(max_length=200)
    body = mongoengine.StringField(required=True)
    # tags = mongoengine.ListField(mongoengine.UUIDField(binary=False))
    files = mongoengine.ListField(mongoengine.UUIDField(binary=False))

    @property
    def shortbody(self) -> str:
        return self.body[0:64]

    meta = {'ordering': ['-id']}  # Descending Order

    # def to_custom_json(self) -> str:
    #     data = json.loads(self.to_json())
    #     data['owner'] = json.loads(self.owner.to_json())
    #     data['category'] = json.loads(self.category.to_json())
    #     data['created'] = self.created.strftime(config.DATETIME_FORMAT_TECHNICAL)
    #     data['modified'] = self.modified.strftime(config.DATETIME_FORMAT_TECHNICAL)
    #     return json.dumps(data)


# Base model frame
class NoteBM(BaseModel):
    numerical_id: Optional[int]
    uuid: Optional[UUID4]
    created: Optional[datetime.datetime]
    modified: Optional[datetime.datetime]
    title: constr(max_length=200)
    body: str
    owner: Optional[UserBM]
    # files: Optional[list]
    # category: Optional[CategoryBM]
    tags: Optional[List[str]]

    class Config:
        orm_mode = True


# Used on json output
# class NoteBM(NoteBM):
#     owner: Optional[UserBM]
#     # files: Optional[list]
#     category: Optional[CategoryBM]
#     tags: Optional[List[str]]

#     class Config:
#         orm_mode = True


# Usen upon note update - added Optional fields
class NoteEditBM(NoteBM):
    uuid: UUID4
    title: Optional[constr(max_length=200)]
    body: Optional[str]
    tags: Optional[list]

    class Config:
        orm_mode = True


class NotesBM(BaseModel):
    __root__: List[NoteBM]  # __root__

    class Config:
        orm_mode = True


class NotesExtendedBM(BaseModel):
    __root__: List[NoteBM]  # __root__

    class Config:
        orm_mode = True
