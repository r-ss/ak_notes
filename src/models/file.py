import json
from datetime import datetime
from typing import Optional, List
from uuid import uuid4

from models.user import UserBM
from models.note import NoteBM

import mongoengine as mongoengine
from pydantic import BaseModel

from config import Config

from filesystem import FileSystemUtils
fs = FileSystemUtils()

class File(mongoengine.Document):
    ''' Represents File attached to Note '''

    linked_to = mongoengine.ReferenceField('Note', required=True)
    uuid = mongoengine.fields.UUIDField(binary=False, default=uuid4, required=True, unique=True)
    created = mongoengine.DateTimeField(default=datetime.utcnow())
    filename = mongoengine.StringField(max_length=256)
    hash = mongoengine.StringField(max_length=16)
    owner = mongoengine.ReferenceField('User', required=True)

    @property
    def path(self) -> str:
        return '%s%s' % (Config.STORAGE['ROOT'], self.filename_uuid)

    @property
    def is_file_exist(self) -> bool:
        return fs.is_file_exist(self.path)
    
    def remove_from_filesystem(self) -> None:
        fs.delete_file(self.path)

    def write_hash(self) -> None:
        self.hash = fs.file_hash(self.path, Config.HASH_DIGEST_SIZE)
        self.save()

    @property
    def file_extension(self) -> str:
        return self.filename.split('.')[-1]

    @property
    def filename_uuid(self) -> str:
        return f'{self.uuid}.{self.file_extension}'

    @property
    def is_file_on_disk_equal_to_saved_hash(self) -> bool:
        if fs.file_hash(self.path, Config.HASH_DIGEST_SIZE) == self.hash:
            return True
        return False

    def to_custom_json(self) -> str:
        data = json.loads(self.to_json())      
        data['linked_to'] = json.loads(self.linked_to.to_custom_json())
        data['owner'] = json.loads(self.owner.to_json())
        return json.dumps(data)


class FileBM(BaseModel):
    uuid: Optional[str]
    linked_to: Optional[NoteBM]
    filename: str = 'default.ext'
    hash: Optional[str]
    owner: Optional[UserBM]


class FilesBM(BaseModel):
    __root__: List[FileBM]    # __root__

class FileEditBM(BaseModel):
    filename: str # yep, only filename can be changed