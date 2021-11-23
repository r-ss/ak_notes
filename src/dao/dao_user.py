from dao.dao import BasicDAOLayer
from models.user import User, UserRegBM, UserBM, UsersBM


class UserDAOLayer(BasicDAOLayer):

    def __init__(self):
        self.target = User
        self.readable = 'User'

    def get(self, response_model=UserBM, **kwargs):
        return super().get(response_model=response_model, **kwargs)

    def get_all(self):
        return super().get_all(response_model=UsersBM)

    def create(self, user: UserRegBM):
        return super().create(user.dict(exclude={'password', 'value'}), response_model=UserBM)
        # return super().create(user, response_model=UserBM)
