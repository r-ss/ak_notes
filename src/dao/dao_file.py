from dao.dao import BasicDAOLayer
from models.file import File, FileBM, FilesBM
from models.note import NoteBM
from models.user import UserBM


class FileDAOLayer(BasicDAOLayer):

    def __init__(self):
        self.target = File
        self.readable = 'File'

    def get(self, response_model=FileBM, **kwargs):
        return super().get(response_model=response_model, **kwargs)

    def get_all(self, response_model=FilesBM):
        return super().get_all(response_model=response_model)

    def get_file_owner(self, **kwargs):
        """ return FileBM with it's owner, UserBM """

        db_file = super().get(response_model=None, **kwargs)
        db_owner = db_file.owner
        return FileBM.from_orm(db_file), UserBM.from_orm(db_owner)

    def get_parent_note(self, **kwargs):
        """ return NoteBM assotiated fith file """

        db_file = super().get(response_model=None, **kwargs)
        db_note = db_file.parent
        return NoteBM.from_orm(db_note)

    def create(self, data: FileBM, response_model=FileBM):
        return super().create(data, response_model=response_model)
