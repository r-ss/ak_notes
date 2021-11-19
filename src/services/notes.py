# from typing import Union
from datetime import datetime

from fastapi import status, HTTPException

from pydantic import UUID4

from models.note import Note, NoteBM, NoteEditBM, NotesBM
from models.category import Category
from models.user import User, UserTokenBM

from services.users.auth import owner_or_admin_can_proceed_only


class NotesService:

    """ CREATE SERVICE """
    def create(note: NoteBM, token: UserTokenBM, category_uuid=None) -> NoteBM:
        """ Create Note """

        db_user = User.objects.get(uuid=token.uuid)

        db_note = Note(
            title=note.title,
            body=note.body
        )
        db_note.save()

        # Assing just created Note under specific or default category
        if category_uuid:
            try:
                category = Category.objects.get(uuid=category_uuid)
            except Category.DoesNotExist:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category does not found')
            owner_or_admin_can_proceed_only(category.owner.uuid, token)

        else:
            category = Category.get_last_for_user(db_user)

        category.notes.append(db_note.uuid)
        category.save()

        return NoteBM.from_orm(db_note)

    """ READ SERVICE """
    def read_specific(uuid: UUID4, token: UserTokenBM) -> NoteBM:
        """ Get single specific note """

        try:
            db_note = Note.objects.get(uuid=uuid)
        except Note.DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note does not found')

        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        return NoteBM.from_orm(db_note)


    def read_all_by_user(token: UserTokenBM) -> NotesBM:
        """ Get all notes owned by current user """

        db_user = User.objects.get(uuid=token.uuid)
        db_categories = Category.objects(uuid__in=db_user.categories)

        # TODO - Refactor following:
        notes_collector = []
        for cat in db_categories:
            db_notes = Note.objects(uuid__in=cat.notes)
            for n in db_notes:
                notes_collector.append(n)
       
        return NotesBM.from_orm(notes_collector)

    # def read_all_with_tag(tag: str, token: UserTokenBM) -> NotesBM:
    #     """ Get all notes by current user that contains specific tag """

    #     db_user = User.objects.get(uuid=token.uuid)
    #     db_notes = Note.objects.filter(owner=db_user, tags__in=[tag])
    #     return NotesBM.from_orm(list(db_notes))

    """ UPDATE SERVICE """
    def update(input_note: NoteEditBM, token: UserTokenBM) -> NoteBM:
        """ Edit note """


        try:
            db_note = Note.objects.get(uuid=input_note.uuid)
        except Note.DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note does not found')

        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        untouched = True

        if input_note.title:
            db_note.title = input_note.title
            untouched = False
        if input_note.body:
            db_note.body = input_note.body
            untouched = False
        # if input_note.tags:
        #     db_note.tags = input_note.tags
        #     untouched = False

        if not untouched:
            db_note.modified = datetime.utcnow()
            db_note.save()
            return NoteBM.from_orm(db_note)
        
        return None

    # def update_note_category(note_uuid: str, new_category: CategoryBM, token: UserTokenBM) -> NoteBM:
    #     """ Change note category """
        
    #     try:
    #         db_note = Note.objects.get(uuid=note_uuid)
    #     except Note.DoesNotExist:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note does not found')

    #     owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

    #     db_category = Category.objects.get(numerical_id=new_category.numerical_id)
    #     db_note.category = db_category
    #     db_note.save()
    #     return NoteBM.from_orm(db_note)

    """ DELETE SERVICE """
    def delete(uuid: str, token: UserTokenBM) -> None:

        try:
            db_note = Note.objects.get(uuid=uuid)
        except Note.DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note does not found')


        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        # print('delete note', db_note)

        db_note.delete()
