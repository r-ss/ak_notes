from typing import Optional

from fastapi_utils.cbv import cbv
from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter

from pydantic import UUID4

from models.note import NoteBM, NoteCreateBM, NotePatchBM
from models.user import UserTokenBM

from services.users.auth import token_required
from services.notes import NotesService

router = InferringRouter(tags=['Notes'])


@cbv(router)
class NotesCBV:

    """ CREATE """
    @router.post('/categories/{category_uuid}/notes', status_code=status.HTTP_201_CREATED, summary='Create note under specific category')
    def create_note_under_specific_category(self, category_uuid: UUID4, note: NoteCreateBM, token: UserTokenBM = Depends(token_required)):
        return NotesService.create(note, token, category_uuid=category_uuid)

    @router.post('/notes', status_code=status.HTTP_201_CREATED, summary='Create note under default category')
    def create_note_under_default_category(self, note: NoteCreateBM, token: UserTokenBM = Depends(token_required)):
        return NotesService.create(note, token)

    """ READ """
    @router.get('/notes/{uuid}', summary='Read one specific note')
    def read_note(self, uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        return NotesService.read_specific(uuid, token)

    @router.get('/notes', summary='Read all notes by current user')
    def read_all_notes_by_user(self,
                       token: UserTokenBM = Depends(token_required),
                       filter: Optional[str] = None,
                       limit: Optional[int] = None,
                       offset: Optional[int] = None
                       ):
        return NotesService.read_all_by_user(token, filter, limit, offset)

    @router.get('/categories/{category_uuid}/notes', summary='Read all notes in specific category')
    def read_all_notes_in_category(self, category_uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        return NotesService.read_all_in_category(token, category_uuid)

    # @router.get('/notes/with-tag/{tag}')
    # def read_with_tag(self, tag: str, token: UserTokenBM = Depends(token_required)):
    #     """ Read all notes by current user that contains specific tag """
    #     return NotesService.read_all_with_tag(tag, token)

    """ UPDATE """
    @router.put('/notes', status_code=status.HTTP_200_OK, summary='Update note')
    def update_note(self, input_note: NoteBM, token: UserTokenBM = Depends(token_required)):
        return NotesService.update(input_note, token)

    @router.patch('/notes/{uuid}', status_code=status.HTTP_200_OK, summary='Update note (patch)')
    def patch_note(self, uuid: UUID4, input_note: NotePatchBM, token: UserTokenBM = Depends(token_required)):
        return NotesService.patch(uuid, input_note, token)

    # @router.put('/notes/{note_uuid}/change-category', status_code=status.HTTP_200_OK)
    # def change_note_category(self, note_uuid: str, new_category: CategoryBM, token: UserTokenBM = Depends(token_required)):
    #     """ change note category """
    #     return NotesService.update_note_category(note_uuid, new_category, token)

    """ DELETE """
    @router.delete('/notes/{uuid}', status_code=status.HTTP_204_NO_CONTENT, summary='Delete note')
    def delete_note(self, uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        return NotesService.delete(uuid, token)
