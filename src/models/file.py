from datetime import datetime
from typing import Optional, List
from uuid import uuid4

import mongoengine as mongoengine
from pydantic import BaseModel, UUID4

from config import config
from models.user import User
from models.category import Category
from models.note import Note
from services.filesystem import FileSystemUtils

import filetype

import os

fs = FileSystemUtils()


class File(mongoengine.Document):
    """ Represents File attached to Note

      ┌───────────────────────────────────┐
      │ Place in app's dataflow:          │
      │                         .-> Tag   │
      │ User -> Category -> Note -> File  │
      │                             ^^^^  │
      └───────────────────────────────────┘
        
        parent: Note
        childrens: None
    """

    uuid = mongoengine.UUIDField(binary=False, default=uuid4, required=True, unique=True)
    created = mongoengine.DateTimeField(default=datetime.utcnow())
    filename = mongoengine.StringField(max_length=256)
    filesize = mongoengine.IntField()
    hash = mongoengine.StringField(max_length=16)
    mime = mongoengine.StringField(max_length=50)

    @property
    def path(self) -> str:
        return '%s%s' % (config.STORAGE['ROOT'], self.filename_uuid)

    @property
    def is_file_exist(self) -> bool:
        return fs.is_file_exist(self.path)


    @property
    def extension(self) -> str:
        return self.filename.split('.')[-1]

    @property
    def filename_uuid(self) -> str:
        return f'{self.uuid}.{self.extension}'

    @property
    def is_file_on_disk_equal_to_saved_hash(self) -> bool:
        if fs.file_hash(self.path, config.HASH_DIGEST_SIZE) == self.hash:
            return True
        return False

    def remove_from_filesystem(self) -> None:
        fs.delete_file(self.path)


    def write_metadata(self) -> None:
        # mime
        kind = filetype.guess(self.path)
        
        if kind is not None:
            self.mime = kind.mime  # filetype lib also have "kind.extension" property

        # filesize    
        self.filesize = str(os.path.getsize(self.path))
        # hash
        self.hash = fs.file_hash(self.path, config.HASH_DIGEST_SIZE)

        del kind

        self.save()

    @property
    def parent(self) -> Note:
        return Note.objects.filter(files__in=[self.uuid])[0]

    @property
    def owner(self) -> User:
        db_note = Note.objects.filter(files__in=[self.uuid])[0]
        db_category = Category.objects.filter(notes__in=[db_note.uuid])[0]
        db_user = User.objects.filter(categories__in=[db_category.uuid])[0]
        return db_user


    meta = {'ordering': ['-id']}  # Descending Order



class FileBM(BaseModel):
    uuid: Optional[UUID4]
    created: Optional[datetime]
    filename: str = 'default.ext'
    filesize: Optional[int]
    hash: Optional[str]
    
    class Config:
        orm_mode = True


class FilesBM(BaseModel):
    __root__: List[FileBM]  # __root__

    class Config:
        orm_mode = True


class FileEditBM(BaseModel):
    uuid: UUID4
    filename: str  # yep, only filename can be changed

    class Config:
        orm_mode = True
