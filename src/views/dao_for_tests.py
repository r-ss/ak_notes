from fastapi_utils.cbv import cbv
from fastapi import status, Depends, HTTPException
from fastapi_utils.inferring_router import InferringRouter

from models.note import NoteBM, NoteCreateBM, NotePatchBM
from models.user import UserTokenBM

from config import config

from pydantic import UUID4

from services.resslogger import RessLogger
log = RessLogger()

from services.dao import NotesDAOService

router = InferringRouter(tags=['DAO'])


@cbv(router)
class DAOLayerCBV:

    """ READ """
    @router.get('/dao', status_code=status.HTTP_200_OK)
    def read_all(self):
        return NotesDAOService.somefunc()
