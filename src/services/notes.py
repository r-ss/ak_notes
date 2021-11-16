from typing import Union
from datetime import datetime

from fastapi import status, HTTPException

from models.note import Note, NoteExtendedBM, NoteEditBM, NotesBM, NotesExtendedBM
from models.category import Category, CategoryBM
from models.user import User, UserTokenBM

from services.users.auth import owner_or_admin_can_proceed_only

import json

class NotesCRUD:

    """ CREATE SERVICE """
    def create(note: NoteExtendedBM, token: UserTokenBM) -> Note:
        """ Create Note """

        db_user = User.objects.get(uuid=token.uuid)
        cat = Category.choose_default()

        db_note = Note(
            title=note.title, body=note.body, owner=db_user, category=cat, tags=note.tags
        )
        db_note.save()
        return db_note.save()

    """ READ SERVICE """
    def read_specific(uuid: str, token: UserTokenBM) -> Union[Note, None]:
        """ Get single specific note """

        try:
            db_note = Note.objects.get(uuid=uuid)
        except Note.DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note does not found')

        print('RE >>>>>>>>>>>>>>>')
        print(type(db_note.uuid))
        print(str(db_note.uuid))

        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        return NoteExtendedBM.from_orm(db_note)

        # return db_note

    def read_all_by_user(token: UserTokenBM) -> Note:
        """ Get all notes owned by current user """

        db_user = User.objects.get(uuid=token.uuid)
        db_notes = Note.objects.filter(owner=db_user)

        # # TODO - Refactor following parse-unparse
        # j = []
        # for n in db_notes:
        #     j.append(json.loads(n.to_custom_json()))

        # print('>>>>>>')
        # print(db_notes.values_list())
        # print(type(list(db_notes)))

        return NotesBM.from_orm(list(db_notes))

    def read_all_with_tag(tag: str, token: UserTokenBM) -> Note:
        """ Get all notes by current user that contains specific tag """

        db_user = User.objects.get(uuid=token.uuid)
        return Note.objects.filter(owner=db_user, tags__in=[tag])

    """ UPDATE SERVICE """
    def update(note_uuid: str, input_note: NoteEditBM, token: UserTokenBM) -> Union[Note, None]:
        """ Edit note """
        db_note = Note.objects.get(uuid=note_uuid)

        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        untouched = True

        if input_note.title:
            db_note.title = input_note.title
            untouched = False
        if input_note.body:
            db_note.body = input_note.body
            untouched = False
        if input_note.tags:
            db_note.tags = input_note.tags
            untouched = False

        if not untouched:
            db_note.modified = datetime.utcnow()
            return db_note.save()
        
        return None

    def update_note_category(note_uuid: str, new_category: CategoryBM, token: UserTokenBM) -> Note:
        """ Change note category """
        db_note = Note.objects.get(uuid=note_uuid)

        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        db_category = Category.objects.get(numerical_id=new_category.numerical_id)
        db_note.category = db_category
        return db_note.save()

    """ DELETE SERVICE """
    def delete(uuid: str, token: UserTokenBM) -> None:
        db_note = Note.objects.get(uuid=uuid)

        

        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        print('delete note', db_note)

        db_note.delete()
