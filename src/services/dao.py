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
    def somefunc():
        print('>>> kek')

        note = NoteDAO.get(uuid=config.TESTNOTE_BY_ALICE_UUID)


        return note
