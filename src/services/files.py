from typing import List
from fastapi import status, HTTPException, UploadFile
from pydantic import UUID4

import filetype
import os

from models.file import FileBM, FileEditBM, FilesBM
from models.user import UserTokenBM

from services.users.auth import check_ownership
from config import config

from services.filesystem import FileSystemUtils

from dao.dao_file import FileDAOLayer
from dao.dao_note import NoteDAOLayer
from dao.dao_user import UserDAOLayer
from dao.dao_category import CategoryDAOLayer

FileDAO = FileDAOLayer()
NoteDAO = NoteDAOLayer()
UserDAO = UserDAOLayer()
CategoryDAO = CategoryDAOLayer()

fs = FileSystemUtils()


class FilesService:

    """CREATE SERVICE"""

    def create(note_uuid: UUID4, uploads: List[UploadFile], token: UserTokenBM) -> FilesBM:
        """Handle multiple uploaded files.
        Saving every uploaded file on local disk.
        Create File item in database, savign hash checksum for file.

        Returns list of oploaded files.
        """

        fs.check_dir(config.STORAGE["UPLOADS"])  # create storage dir on filesystem if not exist

        note, owner = NoteDAO.get_note_owner(uuid=note_uuid)
        check_ownership(owner.uuid, token)

        def collect_and_write_metadata(path: str, file: FileBM) -> None:
            # mime
            kind = filetype.guess(path)
            if kind is not None:
                file.mime = kind.mime  # filetype lib also have "kind.extension" property

            # filesize
            file.filesize = int(os.path.getsize(path))

            # hash
            file.hash = fs.file_hash(path, config.HASH_DIGEST_SIZE)
            del kind
            return FileDAO.update_object(uuid=file.uuid, object=file)

        processed_files_collector = []
        for upload in uploads:
            file = FileDAO.create({"filename": upload.filename})

            filename = f'{file.uuid}.{upload.filename.split(".")[-1]}'

            file_location = "%s%s" % (config.STORAGE["UPLOADS"], filename)
            f = open(file_location, "wb")
            f.write(upload.file.read())
            f.close()

            collect_and_write_metadata(file_location, file)
            processed_files_collector.append(file)

            # update info about files in note
            note.files.append(file.uuid)
            NoteDAO.update_fields(uuid=note.uuid, fields={"files": note.files})

        return FilesBM.parse_obj(processed_files_collector)

    """ READ SERVICE """

    def read_specific(uuid: UUID4, token: UserTokenBM) -> FileBM:
        """Get from db and return single specific file"""

        file, owner = FileDAO.get_file_owner(uuid=uuid)
        check_ownership(owner.uuid, token)

        return file

    def read_all_for_note(note_uuid: UUID4, token: UserTokenBM) -> FilesBM:
        """Get all files attached to specific note"""

        note, owner = NoteDAO.get_note_owner(uuid=note_uuid)
        check_ownership(owner.uuid, token)

        files_collector = []
        for item in note.files:
            file = FileDAO.get(uuid=item)
            files_collector.append(file)

        return FilesBM.from_orm(files_collector)

    def read_all_for_user(token: UserTokenBM) -> FilesBM:
        """Get all files owned by current user"""

        user = UserDAO.get(uuid=token.uuid)
        categories = CategoryDAO.get_all_where(uuid__in=user.categories)

        files_collector = []
        for category in categories:
            notes = NoteDAO.get_all_where(uuid__in=category.notes)
            for note in notes:
                files = FileDAO.get_all_where(uuid__in=note.files)
                for file in files:
                    files_collector.append(file)

        return FilesBM.from_orm(files_collector)

    """ UPDATE SERVICE """

    def update(input_file: FileEditBM, token: UserTokenBM) -> FileBM:
        """Update filename"""

        file, owner = FileDAO.get_file_owner(uuid=input_file.uuid)
        check_ownership(owner.uuid, token)

        if input_file.filename.split(".")[-1] != file.filename.split(".")[-1]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You can't change file extension")

        file.filename = input_file.filename
        return FileDAO.update_fields(uuid=file.uuid, fields={"filename": file.filename})

    """ DELETE SERVICE """

    def delete(uuid: UUID4, token: UserTokenBM) -> None:
        """Delete specific file from filesystem and from database"""

        file, owner = FileDAO.get_file_owner(uuid=uuid)
        check_ownership(owner.uuid, token)

        note = FileDAO.get_parent_note(uuid=file.uuid)

        # update info about file in note
        note.files.remove(file.uuid)
        NoteDAO.update_fields(uuid=note.uuid, fields={"files": note.files})

        filename = f'{file.uuid}.{file.filename.split(".")[-1]}'
        file_location = "%s%s" % (config.STORAGE["UPLOADS"], filename)

        if fs.is_file_exist(file_location):
            fs.delete_file(file_location)
            FileDAO.delete(uuid=file.uuid)
