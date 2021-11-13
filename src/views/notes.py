import json
from datetime import datetime
from fastapi_utils.cbv import cbv
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from models.note import Note, NoteBM, NoteExtendedBM, NoteEditBM, NoteExtendedBM, NotesBM
from models.category import Category, CategoryBM, CategoriesBM
from models.user import User, UserBM, UserTokenBM

router = InferringRouter()

from user_auth import token_required, owner_or_admin_can_proceed_only

@cbv(router)
class NotesCBV:

    ''' CREATE '''
    @router.post("/notes", status_code=status.HTTP_201_CREATED)
    def create(self, note: NoteExtendedBM, token: UserTokenBM = Depends(token_required)):

        db_user = User.objects.get(uuid = token.uuid)

        cat = Category.choose_default()

        db_note = Note(
            title = note.title,
            body = note.body,
            owner = db_user,
            category = cat,
            tags = note.tags
        )
        db_note.save()
        note = NoteExtendedBM.parse_raw(db_note.to_custom_json())
        return note

    ''' READ '''
    @router.get("/notes/{uuid}")
    def read(self, uuid: str, token: UserTokenBM = Depends(token_required)):

        try:
            db_note = Note.objects.get(uuid = uuid)
        except Note.DoesNotExist:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {'message': 'Note does not found'}
            )

        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        note = NoteExtendedBM.parse_raw(db_note.to_custom_json())
        return note

    @router.get("/notes")
    def read_all(self, token: UserTokenBM = Depends(token_required)):

        db_user = User.objects.get(uuid = token.uuid)
        db_notes = Note.objects.filter(owner = db_user)

        # TODO - Refactor following parse-unparse shit
        j = []
        for n in db_notes:
            j.append( json.loads(n.to_custom_json()) )

        notes = NotesBM.parse_obj(j)
        return notes

    ''' UPDATE '''
    @router.put("/notes/{note_uuid}", status_code=status.HTTP_200_OK)
    def update(self, note_uuid: str, input_note: NoteEditBM, token: UserTokenBM = Depends(token_required)):
        db_note = Note.objects.get(uuid = note_uuid)

        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        untouched = True

        if input_note.title:
            db_note.title = input_note.title
            untouched = False
        if input_note.body:
            db_note.body = input_note.body
            untouched = False
        if input_note.tags:
            db_note.tags = input_note.tags
            untouched = False

        if not untouched:
            db_note.modified = datetime.utcnow()
            db_note.save()

            note = NoteExtendedBM.parse_raw(db_note.to_custom_json())
            return note
        else:
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = {'message': 'No data for update'}
            )

    @router.put("/notes/{note_uuid}/change-category", status_code=status.HTTP_200_OK)
    def change_note_categoru(self, note_uuid: str, new_category: CategoryBM, token: UserTokenBM = Depends(token_required)):
        db_note = Note.objects.get(uuid = note_uuid)
        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        db_category = Category.objects.get(numerical_id = new_category.numerical_id)
        db_note.category = db_category
        db_note.save()

        note = NoteExtendedBM.parse_raw(db_note.to_custom_json())
        return note

    ''' DELETE '''
    @router.delete("/notes/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
    def delete(self, uuid: str, token: UserTokenBM = Depends(token_required)):

        

        db_note = Note.objects.get(uuid = uuid)

        owner_or_admin_can_proceed_only(db_note.owner.uuid, token)

        note = NoteExtendedBM.parse_raw(db_note.to_custom_json())

        db_note.delete()
        return {'deteted note': note}

        