from fastapi_utils.cbv import cbv
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from models.user import UserBM, UserRegBM, UserTokenBM
from services.users.auth import is_username_correct, is_password_correct, token_required
from services.users.crud import UsersCRUD

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
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'message': 'Username and password must be provided for registration'}
            )
        if not is_username_correct(user.username):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'message': config.AUTH_USERNAME_REGEX['failmessage']}
            )
        if not is_password_correct(user.password):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'message': config.AUTH_PASSWORD_REGEX['failmessage']}
            )

        db_user = UsersCRUD.create(user)

        user = UserBM.parse_raw(db_user.to_json())

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                'message': 'user registered',
                'username': user.username,
                'uuid': user.uuid,
            }
        )

    """ READ """
    @router.get('/users/{uuid}')
    def read_user(self, uuid: str):

        db_user = UsersCRUD.read(uuid)
        if not db_user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={'message': 'User does not found'},
            )

        return UserBM.parse_raw(db_user.to_json())

    """ UPDATE """
    @router.put('/users/{uuid}')
    def update_user(self, uuid: str, user: UserBM, token: UserTokenBM = Depends(token_required)):

        db_user = UsersCRUD.update(uuid, user, token)

        user = UserBM.parse_raw(db_user.to_json())
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'message': 'Username updated', 'username': user.username},
        )

    """ DELETE """
    @router.delete('/users/{uuid}', status_code=status.HTTP_204_NO_CONTENT)
    def delete_user(self, uuid: str, token: UserTokenBM = Depends(token_required)):

        UsersCRUD.delete(uuid, token)
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={'message': f'User {uuid} deleted'},
        )
