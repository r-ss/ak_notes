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

from dao.dao_test import TestDAOLayer
TestDAO = TestDAOLayer()

class NotesDAOService:

    """ READ SERVICE """
    def read_one(uuid: UUID4):
        # note = TestDAO.get(uuid)
        note = TestDAO.get(351, field='numerical_id')
        return note

    """ READ SERVICE """
    def read_all():
        note = TestDAO.get_all()
        return note

    """ READ SERVICE """
    def postnote(note):
        note = TestDAO.create(note)
        return note

    def delete(uuid):
        note = TestDAO.delete(uuid)
        return note