from fastapi_utils.cbv import cbv
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from models.note import Note, NoteBM, NotesBM
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
        note = NoteBM.parse_raw(db_note.to_json())
        return note

    ''' READ '''
    @router.get("/notes/{numerical_id}")
    def read(self, numerical_id: int):

        try:
            db_note = Note.objects.get(numerical_id = numerical_id)
        except Note.DoesNotExist:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {'message': 'Note does not found'}
            )

        note = NoteBM.parse_raw(db_note.to_custom_json())
        return note

    @router.get("/notes")
    def read_all(self):
        db_notes = Note.objects.all()

        notes = NotesBM.parse_raw(db_notes.to_json())
        return notes    

    ''' UPDATE '''
    @router.put("/notes/{numerical_id}")
    def update(self, numerical_id: int, note: NoteBM):
        db_note = Note.objects.get(numerical_id = numerical_id)
        db_note.name = note.name
        db_note.save()
        note = NoteBM.parse_raw(db_note.to_json())
        return note

    ''' DELETE '''
    @router.delete("/notes/{numerical_id}", status_code=status.HTTP_204_NO_CONTENT)
    def delete(self, numerical_id: int):

        db_note = Note.objects.get(numerical_id = numerical_id)
        note = NoteBM.parse_raw(db_note.to_json())

        db_note.delete()
        return {'deteted note': note}

        