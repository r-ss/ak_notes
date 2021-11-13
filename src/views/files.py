import json
from typing import List
from fastapi_utils.cbv import cbv
from fastapi import status, Depends, HTTPException, UploadFile
from fastapi import File as FastAPIFile
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from models.note import Note
from models.file import File, FileBM, FilesBM, FileEditBM
from models.user import User, UserTokenBM

from user_auth import token_required, owner_or_admin_can_proceed_only
from config import Config


from filesystem import FileSystemUtils
fs = FileSystemUtils()

router = InferringRouter()

@cbv(router)
class FilesCBV:

    ''' CREATE '''
    @router.post("/notes/{note_uuid}/create-file", status_code=status.HTTP_201_CREATED)
    def create(self, note_uuid: str, uploads: List[UploadFile] = FastAPIFile(...), token: UserTokenBM = Depends(token_required)):

        db_user = User.objects.get(uuid = token.uuid)
        fs.check_dir(Config.STORAGE['ROOT']) # create storage dir on filesystem if not exist

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
            db_file = File(
                linked_to = db_note,
                filename = upload.filename,
                owner = db_user
            )
            db_file.save()

            file_location = '%s%s' % (Config.STORAGE['ROOT'], db_file.filename_uuid )
            f = open(file_location, 'wb')
            f.write(upload.file.read())
            f.close()

            db_file.write_hash()
            files_collector.append(json.loads(db_file.to_custom_json()))
            del(db_file)

        uploaded_files = FilesBM.parse_obj(files_collector)
        return uploaded_files

    ''' READ '''
    @router.get("/files/read/{uuid}")
    def read(self, uuid: str, token: UserTokenBM = Depends(token_required)):
        ''' read single specific file '''

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

    @router.get("/files/for-note/{note_uuid}")
    def read_all_for_note(self, note_uuid:str, token:UserTokenBM = Depends(token_required)):
        ''' read all files attached to specific note '''

        db_note = Note.objects.get(uuid = note_uuid)
        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        db_files = File.objects.filter(linked_to = db_note)

        # TODO - Refactor following parse-unparse
        j = []
        for n in db_files:
            j.append( json.loads(n.to_custom_json()) )

        files = FilesBM.parse_obj(j)
        return files

    @router.get("/files/for-user")
    def read_all_for_user(self, token: UserTokenBM = Depends(token_required)):
        ''' read all files owned by current user '''

        db_user = User.objects.get(uuid = token.uuid)

        db_files = File.objects.filter(owner = db_user)

        # TODO - Refactor following parse-unparse
        j = []
        for n in db_files:
            j.append( json.loads(n.to_custom_json()) )

        files = FilesBM.parse_obj(j)
        return files


    # TODO - implement downloads
    # def download():
    # return FileResponse(path)


    ''' UPDATE '''
    @router.put("/files/{uuid}", status_code=status.HTTP_200_OK, response_model=FileBM)
    def update(self, uuid: str, file: FileEditBM, token: UserTokenBM = Depends(token_required)):

        db_file = File.objects.get(uuid = uuid)

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

        