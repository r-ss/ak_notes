import json
from typing import List, Union
from fastapi import status, HTTPException, UploadFile

from models.note import Note
from models.file import File
from models.user import User, UserTokenBM

from services.auth import owner_or_admin_can_proceed_only
from config import Config


from services.filesystem import FileSystemUtils

fs = FileSystemUtils()


def upload_for_note(note_uuid: str, uploads: List[UploadFile], token: UserTokenBM) -> Union[list, None]:

    db_user = User.objects.get(uuid=token.uuid)
    fs.check_dir(Config.STORAGE['ROOT'])  # create storage dir on filesystem if not exist

    try:
        db_note = Note.objects.get(uuid=note_uuid)
    except Note.DoesNotExist:
        return None

    owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

    processed_files_collector = []
    for upload in uploads:
        db_file = File(linked_to=db_note, filename=upload.filename, owner=db_user)
        db_file.save()

        file_location = '%s%s' % (Config.STORAGE['ROOT'], db_file.filename_uuid)
        f = open(file_location, 'wb')
        f.write(upload.file.read())
        f.close()

        db_file.write_hash()
        processed_files_collector.append(json.loads(db_file.to_custom_json()))
        del db_file

    return processed_files_collector


def get_specific(uuid: str, token: UserTokenBM) -> Union[File, None]:
    """ Get single specific file """

    try:
        db_file = File.objects.get(uuid=uuid)
    except File.DoesNotExist:
        return None

    owner_or_admin_can_proceed_only(db_file.owner.uuid, token)
    return db_file


def get_all_for_note(note_uuid: str, token: UserTokenBM) -> File:
    """ Get all files attached to specific note """

    db_note = Note.objects.get(uuid=note_uuid)
    owner_or_admin_can_proceed_only(db_note.owner.uuid, token)
    return File.objects.filter(linked_to=db_note)


def get_all_for_user(token: UserTokenBM) -> File:
    """ Get all files owned by current user """

    db_user = User.objects.get(uuid=token.uuid)
    return File.objects.filter(owner=db_user)


def update(uuid: str, new_filename: str, token: UserTokenBM) -> File:

    db_file = File.objects.get(uuid=uuid)

    owner_or_admin_can_proceed_only(db_file.owner.uuid, token)

    if db_file.file_extension != new_filename.split('.')[-1]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can't change file extension",
        )

    db_file.filename = new_filename
    return db_file.save()


def delete(uuid: str, token: UserTokenBM) -> None:

    db_file = File.objects.get(uuid=uuid)

    owner_or_admin_can_proceed_only(db_file.owner.uuid, token)

    if db_file.is_file_exist and db_file.is_file_on_disk_equal_to_saved_hash:
        db_file.remove_from_filesystem()
        if not db_file.is_file_exist:
            db_file.delete()
