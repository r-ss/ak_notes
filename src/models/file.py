from datetime import datetime
from typing import Optional, List

import mongoengine as mongoengine
from pydantic import BaseModel

from config import Config

from filesystem import FileSystemUtils
fs = FileSystemUtils()

class File(mongoengine.Document):
    # linked_to = mongoengine.ReferenceField('Note', required=False, default='kkekekek')
    created = mongoengine.DateTimeField(default=datetime.utcnow())
    linked_to = mongoengine.StringField(required=False, default='kkekekek')
    filename = mongoengine.StringField(max_length=256)

    @property
    def path(self) -> str:
        return '%s%s' % (Config.STORAGE['ROOT'], self.filename)

    @property
    def is_file_exist(self) -> bool:
        return fs.is_file_exist(self.path)
    
    def remove_from_filesystem(self) -> None:
        fs.delete_file(self.path)


class FileBM(BaseModel):
    linked_to: Optional[str]
    filename: str


class FilesBM(BaseModel):
    __root__: List[FileBM]    # __root__