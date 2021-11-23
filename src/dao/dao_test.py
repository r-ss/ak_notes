from typing import Union
from dao.dao import BasicDAOLayer
from pydantic import UUID4

from models.note import Note, NoteBM, NotesBM


class TestDAOLayer(BasicDAOLayer):

    def __init__(self):
        self.target = Note
        self.readable = 'Note'
    
    def get(self, key = None, field='uuid', response_model=NoteBM, **kwargs):
        print(f'GET key:{key}, field:{field}, kwargs:{kwargs}')



        return super().get(key, field=field, response_model=response_model, **kwargs)

    def get_all(self):
        return super().get_all(response_model=NotesBM)

    def create(self, note: NoteBM):
        return super().create(note, response_model=NoteBM)
