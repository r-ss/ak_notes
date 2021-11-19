from fastapi_utils.cbv import cbv
from fastapi import status, Depends, HTTPException
from fastapi_utils.inferring_router import InferringRouter

from models.user import UserBM, UserRegBM, UserTokenBM
from services.users.auth import is_username_correct, is_password_correct, token_required
from services.users.crud import UsersService

from config import config

from services.resslogger import RessLogger
log = RessLogger()

router = InferringRouter(tags=['Users'])


@cbv(router)
class UsersCBV:

    """ CREATE """
    @router.post('/users', status_code=status.HTTP_201_CREATED)
    def create_user(self, user: UserRegBM):

        if not user.password or not user.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username and password must be provided for registration')
        if not is_username_correct(user.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.AUTH_USERNAME_REGEX['failmessage'])
        if not is_password_correct(user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.AUTH_PASSWORD_REGEX['failmessage'])

        return UsersService.create(user)

    """ READ """
    @router.get('/users/{uuid}', status_code=status.HTTP_200_OK)
    def read_user(self, uuid: str):
        return UsersService.read(uuid)

    """ UPDATE """
    @router.put('/users/{uuid}', status_code=status.HTTP_200_OK, response_model=UserBM)
    def update_user(self, user: UserBM, token: UserTokenBM = Depends(token_required)):
        return UsersService.update(user, token)

    """ DELETE """
    @router.delete('/users/{uuid}', status_code=status.HTTP_204_NO_CONTENT)
    def delete_user(self, uuid: str, token: UserTokenBM = Depends(token_required)):
        UsersService.delete(uuid, token)