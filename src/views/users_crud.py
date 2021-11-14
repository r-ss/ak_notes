from fastapi_utils.cbv import cbv
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from models.user import UserBM, UserRegBM, UserTokenBM
from services.auth import is_username_correct, is_password_correct, token_required
from services.auth import create_user, get_user, update_user, delete_user

from config import Config

from services.resslogger import RessLogger
log = RessLogger()

router = InferringRouter()


@cbv(router)
class UsersCBV:

    """ CREATE """
    @router.post('/user/register', status_code=status.HTTP_201_CREATED)
    def create(self, user: UserRegBM):

        if not user.password or not user.username:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'message': 'Username and password must be provided for registration'}
            )
        if not is_username_correct(user.username):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'message': Config.AUTH_USERNAME_REGEX['failmessage']}
            )
        if not is_password_correct(user.password):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={'message': Config.AUTH_PASSWORD_REGEX['failmessage']}
            )

        db_user = create_user(user)

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
    @router.get('/user/{uuid}')
    def read(self, uuid: str):

        db_user = get_user(uuid)
        if not db_user:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={'message': 'User does not found'},
            )

        return UserBM.parse_raw(db_user.to_json())

    """ UPDATE """
    @router.put('/user/{uuid}')
    def update(self, uuid: str, user: UserBM, token: UserTokenBM = Depends(token_required)):

        db_user = update_user(uuid, user, token)

        user = UserBM.parse_raw(db_user.to_json())
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={'message': 'Username updated', 'username': user.username},
        )

    """ DELETE """
    @router.delete('/user/{uuid}', status_code=status.HTTP_204_NO_CONTENT)
    def delete(self, uuid: str, token: UserTokenBM = Depends(token_required)):

        delete_user(uuid, token)
        return JSONResponse(
            status_code=status.HTTP_204_NO_CONTENT,
            content={'message': f'User {uuid} deleted'},
        )
