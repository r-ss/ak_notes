from dao.dao import BasicDAOLayer
from pydantic import UUID4

from models.user import User, UserBM, UsersBM


class UserDAOLayer(BasicDAOLayer):

    def __init__(self):
        self.target = User
        self.readable = 'User'
    
    def get(self, uuid: UUID4):
        return super().get(uuid, response_model=UserBM)

    def get_all(self):
        return super().get_all(response_model=UsersBM)

    def create(self, user: UserBM):
        return super().create(user, response_model=UserBM)

    # def delete(self, uuid: UUID4):
        # return super().delete(uuid)