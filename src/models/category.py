from typing import Optional, List
from datetime import datetime
from uuid import uuid4

import mongoengine as mongoengine
from pydantic import BaseModel, constr, UUID4

from models.user import User


class Category(mongoengine.Document):
    """ Represents Note Category in database.
        Work / Personal etc

      ┌───────────────────────────────────┐
      │ Place in app's dataflow:          │
      │                         .-> Tag   │
      │ User -> Category -> Note -> File  │
      │         ^^^^^^^^                  │
      └───────────────────────────────────┘
        
        parent: User
        childrens: Note
    """

    numerical_id = mongoengine.SequenceField(unique=True)
    uuid = mongoengine.UUIDField(binary=False, default=uuid4, required=True, unique=True)
    name = mongoengine.StringField(max_length=36)
    created = mongoengine.DateTimeField(default=datetime.utcnow())
    notes = mongoengine.ListField(mongoengine.UUIDField(binary=False), default = [])

    def get_last_for_user(db_user: User):
        """ Used when we create Note without passing category,
            so Note will be created under last User's Category
        """
        return Category.objects.get(uuid=db_user.categories[-1])

    @property
    def parent(self) -> User:
        return self.owner

    @property
    def owner(self) -> User:
        return User.objects.filter(categories__in=[self.uuid])[0]


    meta = {'ordering': ['-id']}  # Descending Order


class CategoryBM(BaseModel):
    """ Pydantic's BaseModel of Category object """

    numerical_id: Optional[int]
    uuid: Optional[UUID4]
    name: Optional[constr(max_length=36)]
    created: Optional[datetime]
    notes: Optional[List[UUID4]] = []
    
    class Config:
        orm_mode = True


class CategoriesBM(BaseModel):
    """ Pydantic's BaseModel of List with Category objects """

    __root__: List[CategoryBM]  # __root__

    class Config:
        orm_mode = True