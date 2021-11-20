from fastapi_utils.cbv import cbv
from fastapi import status, Depends, HTTPException
from fastapi_utils.inferring_router import InferringRouter

from models.user import UserBM, UsersBM, UserRegBM, UserTokenBM
from services.users.auth import Auth, token_required
from services.users.crud import UsersService

from config import config

from pydantic import UUID4

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
        if not Auth.is_username_valid(user.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.AUTH_USERNAME_REGEX['failmessage'])
        if not Auth.is_password_valid(user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=config.AUTH_PASSWORD_REGEX['failmessage'])

        return UsersService.create(user)

    """ READ """
    @router.get('/users', status_code=status.HTTP_200_OK, response_model=UsersBM)
    def read_all(self):
        return UsersService.read_all()

    @router.get('/users/{uuid}', status_code=status.HTTP_200_OK, response_model=UserBM)
    def read_specific(self, uuid: UUID4):
        return UsersService.read_specific(uuid)

    """ UPDATE """
    @router.put('/users/{uuid}', status_code=status.HTTP_200_OK, response_model=UserBM)
    def update_user(self, user: UserBM, token: UserTokenBM = Depends(token_required)):
        return UsersService.update(user, token)

    """ DELETE """
    @router.delete('/users/{uuid}', status_code=status.HTTP_204_NO_CONTENT)
    def delete_user(self, uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        UsersService.delete(uuid, token)
