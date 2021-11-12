from fastapi_utils.cbv import cbv
from fastapi import status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi_utils.inferring_router import InferringRouter

import json

from fastapi import UploadFile
from fastapi import File as FastAPIFile

from models.note import Note, NoteBM
from models.file import File, FileBM, FilesBM, FileEditBM

from models.user import User, UserTokenBM
from user_auth import token_required, owner_or_admin_can_proceed_only

from typing import List

from config import Config


from filesystem import FileSystemUtils
fs = FileSystemUtils()

router = InferringRouter()


@cbv(router)
class FilesCBV:

    ''' CREATE '''
    @router.post("/notes/{note_uuid}/create-file", status_code=status.HTTP_201_CREATED)
    def create(self, note_uuid: str, uploads: List[UploadFile] = FastAPIFile(...), token: UserTokenBM = Depends(token_required)):

        # print(uploads)

        db_user = User.objects.get(uuid = token.uuid)

        fs.check_dir(Config.STORAGE['ROOT'])

        try:
            db_note = Note.objects.get(uuid = note_uuid)
        except Note.DoesNotExist:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {'message': 'Requested Note does not found'}
            )
        
        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)


        files_collector = []

        for upload in uploads:

            # print( upload.filename )
            

            db_file = File(
                linked_to = db_note,
                filename = upload.filename,
                owner = db_user
            )
            db_file.save()

            # filename_uuid = f'{db_file.uuid}.{db_file.file_extension}'

            file_location = '%s%s' % (Config.STORAGE['ROOT'], db_file.filename_uuid )
            f = open(file_location, 'wb')
            f.write(upload.file.read())
            f.close()

            db_file.write_hash()

            files_collector.append(json.loads(db_file.to_custom_json()))

            del(db_file)

        uploaded_files = FilesBM.parse_obj(files_collector)
        
        # file = FileBM.parse_raw(db_file.to_json()) 
        return uploaded_files

    ''' READ '''
    @router.get("/files/{uuid}")
    def read(self, uuid: str, token: UserTokenBM = Depends(token_required)):

        try:
            db_file = File.objects.get(uuid = uuid)
        except File.DoesNotExist:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {'message': 'File does not found'}
            )

        owner_or_admin_can_proceed_only(db_file.owner.uuid, token)

        file = FileBM.parse_raw(db_file.to_custom_json())
        return file

    # TODO - implement downloads
    # @
    # def download()
    # return FileResponse(path)

    @router.get("/files/for-note/{note_uuid}")
    def read_all(self, note_uuid:str, token:UserTokenBM = Depends(token_required)):

        db_note = Note.objects.get(uuid = uuid)
        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        db_files = File.objects.filter(linked_to = db_note)

        files = FilesBM.parse_raw(db_files.to_json())
        return files

    @router.get("/files")
    def read_all(self, token: UserTokenBM = Depends(token_required)):
        ''' read all files owned by current user '''

        # print(token.uuid)

        db_user = User.objects.get(uuid = token.uuid)

        db_files = File.objects.filter(owner = db_user)

        # TODO - Refactor following parse-unparse shit
        j = []
        for n in db_files:
            j.append( json.loads(n.to_custom_json()) )

        files = FilesBM.parse_obj(j)
        return files

    ''' UPDATE '''
    @router.put("/files/{uuid}", status_code=status.HTTP_200_OK, response_model=FileBM)
    def update(self, uuid: str, file: FileEditBM, token: UserTokenBM = Depends(token_required)):

        db_file = File.objects.get(uuid = uuid)
        # file = FileBM.parse_raw(db_file.to_custom_json())

        owner_or_admin_can_proceed_only(db_file.owner.uuid, token)

        if db_file.file_extension != file.filename.split('.')[-1]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't change file extension")

        db_file.filename = file.filename
        db_file.save()

        file = FileBM.parse_raw(db_file.to_custom_json())
        return file

    ''' DELETE '''
    @router.delete("/files/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
    def delete(self, uuid: str, token: UserTokenBM = Depends(token_required)):

        db_file = File.objects.get(uuid = uuid)
        file = FileBM.parse_raw(db_file.to_custom_json())

        owner_or_admin_can_proceed_only(db_file.owner.uuid, token)

        if db_file.is_file_exist and db_file.is_file_on_disk_equal_to_saved_hash:
            db_file.remove_from_filesystem()
            if not db_file.is_file_exist:
                db_file.delete()
                return {'deteted file': file}

        