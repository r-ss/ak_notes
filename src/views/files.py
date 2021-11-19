import json
from typing import List
from fastapi_utils.cbv import cbv
from fastapi import status, Depends, UploadFile
from fastapi import File as FastAPIFile
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from pydantic import UUID4

from models.file import FileBM, FilesBM, FileEditBM
from models.user import UserTokenBM

from services.users.auth import token_required
# from config import config

from services.filesystem import FileSystemUtils
from services.files import FilesService

fs = FileSystemUtils()
router = InferringRouter(tags=['Files'])


@cbv(router)
class FilesCBV:

    """ CREATE """
    @router.post('/notes/{note_uuid}/files', status_code=status.HTTP_201_CREATED)
    def create(self, note_uuid: UUID4, uploads: List[UploadFile] = FastAPIFile(...), token: UserTokenBM = Depends(token_required)):
        return FilesService.create(note_uuid, uploads, token)

    """ READ """
    @router.get('/files/{uuid}')
    def read(self, uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        """ Read single specific file """
        return FilesService.read_specific(uuid, token)

    @router.get('/notes/{note_uuid}/files')
    def read_all_for_note(self, note_uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        """ Read all files attached to specific note """
        return FilesService.read_all_for_note(note_uuid, token)

    @router.get('/users/{user_uuid}/files')
    def read_all_for_user(self, token: UserTokenBM = Depends(token_required)):
        """ Read all files owned by current user """
        return FilesService.read_all_for_user(token)

    """ UPDATE """
    @router.put('/files/{uuid}', status_code=status.HTTP_200_OK, response_model=FileBM)
    def update_file(self, file: FileEditBM, token: UserTokenBM = Depends(token_required)):
        """ Method to edit file, now only filename can be changed """
        return FilesService.update(file, token)

    """ DELETE """
    @router.delete('/files/{uuid}', status_code=status.HTTP_204_NO_CONTENT)
    def delete_file(self, uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        FilesService.delete(uuid, token)
        return {'file deleted'}
