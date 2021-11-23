from dao.dao import BasicDAOLayer
from models.note import Note, NoteBM, NotesBM
from models.user import UserBM
from mongoengine.queryset.visitor import Q as mongo_Q


class NoteDAOLayer(BasicDAOLayer):

    def __init__(self):
        self.target = Note
        self.readable = 'Note'

    def get(self, response_model=NoteBM, **kwargs):
        return super().get(response_model=response_model, **kwargs)

    def get_all(self):
        return super().get_all(response_model=NotesBM)

    def get_note_owner(self, **kwargs):
        """ return NoteBM with it's owner, UserBM """

        db_note = super().get(response_model=None, **kwargs)
        db_owner = db_note.owner
        return NoteBM.from_orm(db_note), UserBM.from_orm(db_owner)

    def create(self, note: NoteBM):
        return super().create(note, response_model=NoteBM)

    def get_all_where(self, **kwargs):
        return super().get_all_where(response_model=NotesBM, **kwargs)

    def search_notes(self, notes_list, filter):
        db_notes = super().get_all_where(uuid__in=notes_list)
        db_notes = db_notes.filter(mongo_Q(title__contains=filter) | mongo_Q(body__contains=filter))
        return NotesBM.from_orm(list(db_notes))
