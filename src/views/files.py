import json
from typing import List
from fastapi_utils.cbv import cbv
from fastapi import status, Depends, UploadFile
from fastapi import File as FastAPIFile
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from models.file import FileBM, FilesBM, FileEditBM
from models.user import UserTokenBM

from services.users.auth import token_required
# from config import Config


from services.filesystem import FileSystemUtils

from services.files_logic import upload_for_note, get_specific, get_all_for_note, get_all_for_user, update, delete


fs = FileSystemUtils()

router = InferringRouter()


@cbv(router)
class FilesCBV:

    """ CREATE """
    @router.post('/notes/{note_uuid}/create-file', status_code=status.HTTP_201_CREATED)
    def create(self, note_uuid: str, uploads: List[UploadFile] = FastAPIFile(...), token: UserTokenBM = Depends(token_required)):
        uploaded_files = upload_for_note(note_uuid, uploads, token)
        return FilesBM.parse_obj(uploaded_files)

    """ READ """
    @router.get('/files/read/{uuid}')
    def read(self, uuid: str, token: UserTokenBM = Depends(token_required)):
        """ Read single specific file """

        db_file = get_specific(uuid, token)
        if not db_file:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={'message': 'File does not found'},
            )
        return FileBM.parse_raw(db_file.to_custom_json())

    @router.get('/files/for-note/{note_uuid}')
    def read_all_for_note(self, note_uuid: str, token: UserTokenBM = Depends(token_required)):
        """ Read all files attached to specific note """

        db_files = get_all_for_note(note_uuid, token)

        # TODO - Refactor following parse-unparse
        j = []
        for n in db_files:
            j.append(json.loads(n.to_custom_json()))

        return FilesBM.parse_obj(j)

    @router.get('/files/for-user')
    def read_all_for_user(self, token: UserTokenBM = Depends(token_required)):
        """ Read all files owned by current user """

        db_files = get_all_for_user(token)

        # TODO - Refactor following parse-unparse
        j = []
        for n in db_files:
            j.append(json.loads(n.to_custom_json()))

        return FilesBM.parse_obj(j)

    # TODO - implement downloads
    # def download():
    # return FileResponse(path)

    """ UPDATE """
    @router.put('/files/{uuid}', status_code=status.HTTP_200_OK, response_model=FileBM)
    def update_file(self, uuid: str, file: FileEditBM, token: UserTokenBM = Depends(token_required)):
        """ Method to edit file, now only filename can be changed """
        db_file = update(uuid, file.filename, token)
        return FileBM.parse_raw(db_file.to_custom_json())

    """ DELETE """
    @router.delete('/files/{uuid}', status_code=status.HTTP_204_NO_CONTENT)
    def delete_file(self, uuid: str, token: UserTokenBM = Depends(token_required)):

        delete(uuid, token)

        return {'file deleted'}
