import json
from datetime import datetime
from fastapi_utils.cbv import cbv
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from models.note import Note, NoteBM, NoteExtendedBM, NoteEditBM, NoteExtendedBM, NotesBM
from models.tag import Tag, TagBM, TagsBM
from models.category import Category, CategoryBM, CategoriesBM
from models.user import User, UserBM

router = InferringRouter()

@cbv(router)
class NotesCBV:

    ''' CREATE '''
    @router.post("/notes", status_code=status.HTTP_201_CREATED)
    def create(self, note: NoteBM):

        # default user and category
        usr = User.objects.get(uuid = '23ca15f6-990a-4483-ab6a-db63c0c3545e')
        cat = Category.objects.get(numerical_id = 5)

        db_note = Note(
            title = note.title,
            body = note.body,
            owner = usr,
            category = cat
        )
        db_note.save()
        note = NoteExtendedBM.parse_raw(db_note.to_custom_json())
        return note

    ''' READ '''
    @router.get("/notes/{uuid}")
    def read(self, uuid: str):

        try:
            db_note = Note.objects.get(uuid = uuid)
        except Note.DoesNotExist:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {'message': 'Note does not found'}
            )

        note = NoteExtendedBM.parse_raw(db_note.to_custom_json())
        return note

    @router.get("/notes")
    def read_all(self):
        db_notes = Note.objects.all()

        # TODO - Refactor following parse-unparse shit
        j = []
        for n in db_notes:
            j.append( json.loads(n.to_custom_json()) )

        notes = NotesBM.parse_obj(j)
        return notes

    ''' UPDATE '''
    @router.put("/notes/{uuid}")
    def update(self, uuid: str, note: NoteEditBM):
        db_note = Note.objects.get(uuid = uuid)

        db_note.title = note.title
        # db_note.body = note.body
        db_note.modified = datetime.utcnow()
        db_note.save()

        note = NoteExtendedBM.parse_raw(db_note.to_custom_json())
        return note

    ''' DELETE '''
    @router.delete("/notes/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
    def delete(self, uuid: str):

        db_note = Note.objects.get(uuid = uuid)
        note = NoteExtendedBM.parse_raw(db_note.to_custom_json())

        db_note.delete()
        return {'deteted note': note}

        