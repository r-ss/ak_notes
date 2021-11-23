from typing import Union
from dao.dao import BasicDAOLayer
from pydantic import UUID4

from models.user import User, UserRegBM, UserBM, UsersBM


class UserDAOLayer(BasicDAOLayer):

    def __init__(self):
        self.target = User
        self.readable = 'User'
    
    def get(self, key: Union[UUID4, str] = None, field='uuid', response_model=UserBM, **kwargs):
        return super().get(key, field=field, response_model=response_model, **kwargs)

    def get_all(self):
        return super().get_all(response_model=UsersBM)

    def create(self, user: UserRegBM):
        return super().create(user.dict(exclude={'password', 'value'}), response_model=UserBM)
        # return super().create(user, response_model=UserBM)
