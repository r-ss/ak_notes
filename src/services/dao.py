# from typing import Union
from datetime import datetime

from fastapi import status, HTTPException

from pydantic import UUID4

from models.note import Note, NoteBM, NoteCreateBM, NotePatchBM, NotesBM
from models.category import Category
from models.user import User, UserTokenBM

from config import config

from services.users.auth import owner_or_admin_can_proceed_only

from mongoengine.queryset.visitor import Q as mongo_Q

from dao.dao_note import NoteDAOLayer
NoteDAO = NoteDAOLayer()

class NotesDAOService:

    """ READ SERVICE """
    def read_one(uuid):
        note = NoteDAO.get(uuid)
        return note

    """ READ SERVICE """
    def read_all():
        note = NoteDAO.get_all()
        return note

    """ READ SERVICE """
    def postnote(note):
        note = NoteDAO.create(note)
        return note

    def delete(uuid):
        note = NoteDAO.delete(uuid)
        return note