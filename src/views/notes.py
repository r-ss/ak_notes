import json
from fastapi_utils.cbv import cbv
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from models.note import NoteExtendedBM, NoteEditBM, NoteExtendedBM, NotesExtendedBM
from models.category import CategoryBM
from models.user import UserTokenBM

from services.users.auth import token_required, owner_or_admin_can_proceed_only
from services.notes import NotesCRUD

router = InferringRouter(tags=['Notes'])


@cbv(router)
class NotesCBV:

    """ CREATE """
    @router.post('/notes', status_code=status.HTTP_201_CREATED)
    def create_note(self, note: NoteExtendedBM, token: UserTokenBM = Depends(token_required)):
        db_note = NotesCRUD.create(note, token)
        return NoteExtendedBM.parse_raw(db_note.to_custom_json())

    """ READ """
    @router.get('/notes/{uuid}')
    def read_note(self, uuid: str, token: UserTokenBM = Depends(token_required)):
        """ Read single specific note """
        db_note = NotesCRUD.read_specific(uuid)
        if not db_note:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={'message': 'Note does not found'},
            )
        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)
        return NoteExtendedBM.parse_raw(db_note.to_custom_json())

    @router.get('/notes')
    def read_all_notes(self, token: UserTokenBM = Depends(token_required)):
        """ Read all notes owned by current user """

        db_notes = NotesCRUD.read_all_by_user(token)

        # TODO - Refactor following parse-unparse
        j = []
        for n in db_notes:
            j.append(json.loads(n.to_custom_json()))

        return NotesExtendedBM.parse_obj(j)

    @router.get('/notes/with-tag/{tag}')
    def read_with_tag(self, tag: str, token: UserTokenBM = Depends(token_required)):
        """ Read all notes by current user that contains specific tag """

        db_notes = NotesCRUD.read_all_with_tag(tag, token)

        # TODO - Refactor following parse-unparse
        j = []
        for n in db_notes:
            j.append(json.loads(n.to_custom_json()))

        return NotesExtendedBM.parse_obj(j)

    """ UPDATE """
    @router.put('/notes/{note_uuid}', status_code=status.HTTP_200_OK)
    def update(self, note_uuid: str, input_note: NoteEditBM, token: UserTokenBM = Depends(token_required)):
        """ Edit note """

        db_note = NotesCRUD.update(note_uuid, input_note, token)

        if not db_note:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'message': 'No data for update'},
            )
        return NoteExtendedBM.parse_raw(db_note.to_custom_json())

    @router.put('/notes/{note_uuid}/change-category', status_code=status.HTTP_200_OK)
    def change_note_category(self, note_uuid: str, new_category: CategoryBM, token: UserTokenBM = Depends(token_required)):
        """ change note category """
        db_note = NotesCRUD.update_note_category(note_uuid, new_category, token)
        return NoteExtendedBM.parse_raw(db_note.to_custom_json())

    """ DELETE """
    @router.delete('/notes/{uuid}', status_code=status.HTTP_204_NO_CONTENT)
    def delete_note(self, uuid: str, token: UserTokenBM = Depends(token_required)):
        NotesCRUD.delete(uuid, token)
        return {'note deleted'}
