from typing import List
from fastapi import status, HTTPException, UploadFile
from models.category import Category

from pydantic import UUID4

from models.note import Note
from models.file import File, FileBM, FileEditBM, FilesBM
from models.user import User, UserTokenBM

from services.users.auth import owner_or_admin_can_proceed_only
from config import config

from services.filesystem import FileSystemUtils

fs = FileSystemUtils()


class FilesService:

    """ CREATE SERVICE """
    def create(note_uuid: UUID4, uploads: List[UploadFile], token: UserTokenBM) -> FilesBM:
        """ Handle multiple uploaded files.
            Saving every uploaded file on local disk.
            Create File item in database, savign hash checksum for file.

            Returns list of oploaded files.
        """

        db_user = User.objects.get(uuid=token.uuid)
        fs.check_dir(config.STORAGE['ROOT'])  # create storage dir on filesystem if not exist

        try:
            db_note = Note.objects.get(uuid=note_uuid)
        except Note.DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note does not found')

        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        processed_files_collector = []
        for upload in uploads:
            db_file = File(filename=upload.filename)
            db_file.save()

            file_location = '%s%s' % (config.STORAGE['ROOT'], db_file.filename_uuid)
            f = open(file_location, 'wb')
            f.write(upload.file.read())
            f.close()

            db_file.write_metadata()
            processed_files_collector.append(FileBM.from_orm(db_file))
        
            # update info about files in note
            db_note.files.append(db_file.uuid)
            db_note.save()

            del db_file

        return FilesBM.parse_obj(processed_files_collector)

    """ READ SERVICE """
    def read_specific(uuid: UUID4, token: UserTokenBM) -> FileBM:
        """ Get from db and return single specific file """

        try:
            db_file = File.objects.get(uuid=uuid)
        except File.DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File does not found')

        owner_or_admin_can_proceed_only(db_file.owner.uuid, token)
        return FileBM.from_orm(db_file)

    def read_all_for_note(note_uuid: UUID4, token: UserTokenBM) -> FilesBM:
        """ Get all files attached to specific note """

        db_note = Note.objects.get(uuid=note_uuid)

        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        files_collector = []
        for item in db_note.files:
            db_file = File.objects.get(uuid=item)
            files_collector.append(FileBM.from_orm(db_file))

        return FilesBM.from_orm(files_collector)

    def read_all_for_user(token: UserTokenBM) -> FilesBM:
        """ Get all files owned by current user """

        # TODO - check permissions
        db_user = User.objects.get(uuid=token.uuid)
        db_categories = Category.objects(uuid__in=db_user.categories)

        # TODO - refactor following
        files_collector = []
        for cat in db_categories:
            db_notes = Note.objects(uuid__in=cat.notes)
            for note in db_notes:
                for file_uuid in note.files:
                    db_file = File.objects(uuid__in=file_uuid)
                    files_collector.append(FileBM.from_orm(db_file))

        # files_collector = []
        # for db_note in db_notes:
        #     for item in db_note.files:
        #         try:
        #             db_file = File.objects.get(uuid=item)
        #         except File.DoesNotExist:
        #             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='File does not found')
        #         files_collector.append(FileBM.from_orm(db_file))

        return FilesBM.parse_obj(files_collector)

    """ UPDATE SERVICE """
    def update(file: FileEditBM, token: UserTokenBM) -> FileBM:
        """ Update filename """

        db_file = File.objects.get(uuid=file.uuid)

        # TODO - check permissions
        owner_or_admin_can_proceed_only(db_file.owner.uuid, token)

        if db_file.extension != file.filename.split('.')[-1]:
            raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="You can't change file extension")

        db_file.filename = file.filename
        return FileBM.from_orm(db_file.save())

    """ DELETE SERVICE """
    def delete(uuid: UUID4, token: UserTokenBM) -> None:
        """ Delete specific file from filesystem and from database """

        db_file = File.objects.get(uuid=uuid)

        # TODO - check permissions
        owner_or_admin_can_proceed_only(db_file.owner.uuid, token)

        # update info about file in note
        db_note = db_file.parent
        db_note.files.remove(db_file.uuid)
        db_note.save()

        if db_file.is_file_exist and db_file.is_file_on_disk_equal_to_saved_hash:
            db_file.remove_from_filesystem()
            if not db_file.is_file_exist:
                db_file.delete()


