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
    @router.get('/dao/one/{uuid}', status_code=status.HTTP_200_OK)
    def read_one(self, uuid:UUID4):
        return NotesDAOService.read_one(uuid)

    """ READ """
    @router.get('/dao/all', status_code=status.HTTP_200_OK)
    def read_all(self):
        return NotesDAOService.read_all()


    @router.post('/dao', status_code=status.HTTP_201_CREATED)
    def postooo(self, note: NoteCreateBM):
        return NotesDAOService.postnote(note)

    @router.delete('/dao/{uuid}', status_code=status.HTTP_200_OK)
    def delete(self, uuid:UUID4):
        return NotesDAOService.delete(uuid)