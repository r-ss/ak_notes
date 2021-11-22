# from typing import Union
from datetime import datetime

from fastapi import status, HTTPException

from pydantic import UUID4

from models.note import Note, NoteBM, NoteCreateBM, NotePatchBM, NotesBM
from models.category import Category
from models.user import User, UserBM, UserTokenBM

from services.users.auth import owner_or_admin_can_proceed_only

from mongoengine.queryset.visitor import Q as mongo_Q



class BasicDAOLayer:

    def __init__(self):
        self.target = None
        self.readable = '--EMPTY--'


    """ GET """
    def get(self, key, field='uuid', response_model=None):

        print('response_model', response_model)

        try:
            db_obj = self.target.objects.get(__raw__={field:key})
        except self.target.DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{self.readable} does not found')

        print('type', type(db_obj))
        print('db_obj', db_obj)

        if response_model:
            return response_model.from_orm(db_obj)
        return db_obj


class NoteDAOLayer(BasicDAOLayer):

    def __init__(self):
        # super().__init__()
        self.target = User
        self.readable = 'User'
        
    
    """ GET """
    def get(self, uuid: UUID4):
        return super().get('Alice', field='username', response_model=UserBM)
