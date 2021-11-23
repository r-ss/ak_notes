from datetime import datetime
from fastapi import status, HTTPException
from pydantic import UUID4

from models.note import NoteBM, NoteCreateBM, NotePatchBM, NotesBM
from models.user import UserTokenBM
from services.users.auth import check_ownership

from dao.dao_note import NoteDAOLayer
from dao.dao_user import UserDAOLayer
from dao.dao_category import CategoryDAOLayer

NoteDAO = NoteDAOLayer()
UserDAO = UserDAOLayer()
CategoryDAO = CategoryDAOLayer()


class NotesService:

    """ CREATE SERVICE """
    def create(note_input: NoteCreateBM, token: UserTokenBM, category_uuid: UUID4 = None) -> NoteBM:
        """ Create Note """

        user = UserDAO.get(uuid=token.uuid)
        note_created = NoteDAO.create(note_input)

        # Assing just created Note under specific or default category
        if category_uuid:
            category = CategoryDAO.get(uuid=category_uuid)
            # TODO - check_ownership(category.owner.uuid, token)
        else:
            category = CategoryDAO.get_last_for_user(user)

        category.notes.append(note_created.uuid)
        CategoryDAO.update_fields(uuid=category.uuid, fields={'notes': category.notes})
        return note_created

    """ READ SERVICE """
    def read_specific(uuid: UUID4, token: UserTokenBM) -> NoteBM:
        """ Get single specific note """
        note, owner = NoteDAO.get_note_owner(uuid=uuid)
        check_ownership(owner.uuid, token)
        return note

    def read_all_by_user(token: UserTokenBM, filter=None, limit=None, offset=None) -> NotesBM:
        """ Get all notes owned by current user """

        user = UserDAO.get(uuid=token.uuid)
        categories = CategoryDAO.get_all_where(uuid__in=user.categories)

        notes_collector = []
        for cat in categories:
            notes = NoteDAO.get_all_where(uuid__in=cat.notes)

            if filter:
                notes = NoteDAO.search_notes(cat.notes, filter)

            for n in notes:
                notes_collector.append(n)

        # Pagination
        if offset:
            if (limit + offset) > len(notes_collector):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="We don't have so much Notes")
            notes_collector = notes_collector[offset: limit + offset]

        return NotesBM.parse_obj(notes_collector)

    def read_all_in_category(token: UserTokenBM, category_uuid=UUID4) -> NotesBM:
        """ Get all notes in specific category """

        user = UserDAO.get(uuid=token.uuid)
        if category_uuid not in user.categories:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not allowed")

        category = CategoryDAO.get(uuid=category_uuid)

        notes = NoteDAO.get_all_where(uuid__in=category.notes)

        return notes

    def read_all_with_tag(tag_uuid: UUID4, token: UserTokenBM) -> NotesBM:
        """ Get all notes by current user that contains specific tag """

        user = UserDAO.get(uuid=token.uuid)
        categories = CategoryDAO.get_all_where(uuid__in=user.categories)

        notes_collector = []
        for category in categories:
            notes = NoteDAO.get_all_where(uuid__in=category.notes)
            for note in notes:
                if tag_uuid in note.tags:
                    notes_collector.append(note)

        return NotesBM.parse_obj(notes_collector)

    """ UPDATE SERVICE """
    def update(input_note: NoteBM, token: UserTokenBM) -> NoteBM:
        """ Edit note """

        note, owner = NoteDAO.get_note_owner(uuid=input_note.uuid)
        check_ownership(owner.uuid, token)

        fields_dict = {}
        if input_note.title:
            fields_dict['title'] = input_note.title
        if input_note.body:
            fields_dict['body'] = input_note.body

        if len(fields_dict) >= 1:
            fields_dict['modified'] = datetime.utcnow()
            return NoteDAO.update_fields(uuid=note.uuid, fields=fields_dict, response_model=NoteBM)

    """ PATCH SERVICE """
    def patch(note_uuid: UUID4, input_note: NotePatchBM, token: UserTokenBM) -> NoteBM:
        """ Edit note """

        if input_note.uuid and input_note.uuid != note_uuid:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Notes UUIDs confusion')

        note, owner = NoteDAO.get_note_owner(uuid=note_uuid)
        check_ownership(owner.uuid, token)

        fields_dict = {}
        if input_note.title:
            fields_dict['title'] = input_note.title
        if input_note.body:
            fields_dict['body'] = input_note.body

        if len(fields_dict) >= 1:
            fields_dict['modified'] = datetime.utcnow()
            return NoteDAO.update_fields(uuid=note_uuid, fields=fields_dict, response_model=NoteBM)

    # def update_note_category(note_uuid: str, new_category: CategoryBM, token: UserTokenBM) -> NoteBM:
    #     """ Change note category """

    #     try:
    #         db_note = Note.objects.get(uuid=note_uuid)
    #     except Note.DoesNotExist:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Note does not found')

    #     check_ownership(db_note.owner.uuid, token)

    #     db_category = Category.objects.get(numerical_id=new_category.numerical_id)
    #     db_note.category = db_category
    #     db_note.save()
    #     return NoteBM.from_orm(db_note)

    """ DELETE SERVICE """
    def delete(uuid: UUID4, token: UserTokenBM) -> None:

        user = UserDAO.get(uuid=token.uuid)
        categories = CategoryDAO.get_all_where(uuid__in=user.categories)

        note, owner = NoteDAO.get_note_owner(uuid=uuid)
        check_ownership(owner.uuid, token)

        for cat in categories:
            if note.uuid in cat.notes:
                cat.notes.remove(note.uuid)
                CategoryDAO.update_fields(uuid=cat.uuid, fields={'notes': cat.notes})
                break

        NoteDAO.delete(uuid=note.uuid)
