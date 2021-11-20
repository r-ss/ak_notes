from typing import Optional

from fastapi_utils.cbv import cbv
from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter

from pydantic import UUID4

from models.note import NoteBM, NoteEditBM
# from models.category import CategoryBM
from models.user import UserTokenBM

from services.users.auth import token_required
from services.notes import NotesService


router = InferringRouter(tags=['Notes'])


@cbv(router)
class NotesCBV:

    """ CREATE """
    @router.post('/categories/{category_uuid}/notes', status_code=status.HTTP_201_CREATED, summary='Create Note under specific Category')
    def create_note_under_specific_category(self, category_uuid: UUID4, note: NoteBM, token: UserTokenBM = Depends(token_required)):
         return NotesService.create(note, token, category_uuid=category_uuid)

    @router.post('/notes', status_code=status.HTTP_201_CREATED, summary='Create Note under default Category')
    def create_note_under_default_category(self, note: NoteBM, token: UserTokenBM = Depends(token_required)):
        return NotesService.create(note, token)

    """ READ """
    @router.get('/notes/{uuid}')
    def read_note(self, uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        """ Read one specific """
        return NotesService.read_specific(uuid, token)

    @router.get('/notes')
    def read_all_notes(self,
                       token: UserTokenBM = Depends(token_required),
                       filter: Optional[str] = None,
                       limit: Optional[int] = None,
                       offset: Optional[int] = None
                       ):
        """ Read all by current user """
        return NotesService.read_all_by_user(token, filter, limit, offset)

    # @router.get('/notes/with-tag/{tag}')
    # def read_with_tag(self, tag: str, token: UserTokenBM = Depends(token_required)):
    #     """ Read all notes by current user that contains specific tag """
    #     return NotesService.read_all_with_tag(tag, token)

    """ UPDATE """
    @router.put('/notes', status_code=status.HTTP_200_OK, summary='Update one specific Note')
    def update(self, input_note: NoteEditBM, token: UserTokenBM = Depends(token_required)):
        return NotesService.update(input_note, token)

    # @router.put('/notes/{note_uuid}/change-category', status_code=status.HTTP_200_OK)
    # def change_note_category(self, note_uuid: str, new_category: CategoryBM, token: UserTokenBM = Depends(token_required)):
    #     """ change note category """
    #     return NotesService.update_note_category(note_uuid, new_category, token)

    """ DELETE """
    @router.delete('/notes/{uuid}', status_code=status.HTTP_204_NO_CONTENT)
    def delete_note(self, uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        return NotesService.delete(uuid, token)
