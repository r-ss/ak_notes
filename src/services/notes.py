# from typing import Union
from datetime import datetime

from fastapi import status, HTTPException

from pydantic import UUID4

from models.note import Note, NoteBM, NoteCreateBM, NotePatchBM, NotesBM
from models.category import Category
from models.user import User, UserTokenBM

from services.users.auth import owner_or_admin_can_proceed_only

# from mongoengine.queryset.visitor import Q as mongo_Q

from dao.dao_note import NoteDAOLayer
from dao.dao_user import UserDAOLayer
from dao.dao_category import CategoryDAOLayer

NoteDAO = NoteDAOLayer()
UserDAO = UserDAOLayer()
CategoryDAO = CategoryDAOLayer()


class NotesService:

    """ CREATE SERVICE """
    def create(note_input: NoteCreateBM, token: UserTokenBM, category_uuid:UUID4=None) -> NoteBM:
        """ Create Note """

        user = UserDAO.get(token.uuid)
        note_created = NoteDAO.create(note_input)

        # Assing just created Note under specific or default category
        if category_uuid:
            category = CategoryDAO.get(category_uuid)
            # owner_or_admin_can_proceed_only(category.owner.uuid, token)
        else:
            category = CategoryDAO.get_last_for_user(user)

        # print(type(category))
        # print(category)

        category.notes.append(note_created.uuid)

        # print('category.notes', category.notes)
        CategoryDAO.update_fields(category.uuid, fields_dict={'notes': category.notes})

        return note_created

    """ READ SERVICE """
    def read_specific(uuid: UUID4, token: UserTokenBM) -> NoteBM:
        """ Get single specific note """
        note, owner = NoteDAO.get_note_owner(uuid)

        if owner.uuid != token.uuid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Seems like you are not authorized to this',
            )

        return note


    def read_all_by_user(token: UserTokenBM, filter=None, limit=None, offset=None) -> NotesBM:
        """ Get all notes owned by current user """

        user = UserDAO.get(token.uuid)
        categories = CategoryDAO.get_all_where(uuid__in=user.categories)


        notes_collector = []
        for cat in categories:
            notes = NoteDAO.get_all_where(uuid__in=cat.notes)

            if filter:
                notes = NoteDAO.search_notes(cat.notes, filter)

            # TODO limit and offset
            # if limit and offset:
            #     if (limit + offset) > db_notes.count():
            #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="We don't have so much Notes")
            #     db_notes = db_notes[offset: limit + offset]

            for n in notes:
                notes_collector.append(n)

        if offset:
            if (limit + offset) > len(notes_collector):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="We don't have so much Notes")
            notes_collector = notes_collector[offset: limit + offset]

        return NotesBM.parse_obj(notes_collector)


    def read_all_in_category(token: UserTokenBM, category_uuid=UUID4) -> NotesBM:
        """ Get all notes in specific category """

        user = UserDAO.get(token.uuid)
        if category_uuid not in user.categories:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not allowed")

        category = CategoryDAO.get(category_uuid)
        
        notes = NoteDAO.get_all_where(uuid__in=category.notes)

        return notes

    # def read_all_with_tag(tag: str, token: UserTokenBM) -> NotesBM:
    #     """ Get all notes by current user that contains specific tag """

    #     db_user = User.objects.get(uuid=token.uuid)
    #     db_notes = Note.objects.filter(owner=db_user, tags__in=[tag])
    #     return NotesBM.from_orm(list(db_notes))

    """ UPDATE SERVICE """
    def update(input_note: NoteBM, token: UserTokenBM) -> NoteBM:
        """ Edit note """

        note, owner = NoteDAO.get_note_owner(input_note.uuid)

        if owner.uuid != token.uuid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Seems like you are not authorized to this',
            )

        fields_dict={}
        if input_note.title:
            fields_dict['title'] = input_note.title
        if input_note.body:
            fields_dict['body'] = input_note.body

        if len(fields_dict) >= 1:
            fields_dict['modified'] = datetime.utcnow()
            return NoteDAO.update_fields(note.uuid, fields_dict=fields_dict, response_model=NoteBM)


    """ PATCH SERVICE """
    def patch(note_uuid: UUID4, input_note: NotePatchBM, token: UserTokenBM) -> NoteBM:
        """ Edit note """

        if input_note.uuid and input_note.uuid != note_uuid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Notes UUIDs confusion')

        note, owner = NoteDAO.get_note_owner(note_uuid)

        if owner.uuid != token.uuid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Seems like you are not authorized to this',
            )

        fields_dict={}
        if input_note.title:
            fields_dict['title'] = input_note.title
        if input_note.body:
            fields_dict['body'] = input_note.body

        if len(fields_dict) >= 1:
            fields_dict['modified'] = datetime.utcnow()
            return NoteDAO.update_fields(note_uuid, fields_dict=fields_dict, response_model=NoteBM)


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
    def delete(uuid: UUID4, token: UserTokenBM) -> None:

        user = UserDAO.get(token.uuid)
        categories = CategoryDAO.get_all_where(uuid__in=user.categories)

        note, owner = NoteDAO.get_note_owner(uuid)

        # print(note)
        if owner.uuid != token.uuid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Seems like you are not authorized to this',
            )

        for cat in categories:
            if note.uuid in cat.notes:
                cat.notes.remove(note.uuid)
                CategoryDAO.update_fields(cat.uuid, fields_dict={'notes':cat.notes})
                break

        NoteDAO.delete(note.uuid)
