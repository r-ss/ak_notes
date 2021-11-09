from fastapi_utils.cbv import cbv
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

import datetime
from re import compile

import bcrypt
import jwt

from models.user import User, UserBM

router = InferringRouter()

from resslogger import RessLogger
log = RessLogger()

USERNAME_REGEX = compile(r'\A[\w\-\.]{4,}\Z')
PASSWORD_REGEX = compile(r'\A[\w\-\.]{6,}\Z')

# checking username for valid characters
def username_pass_regex(username):
    return USERNAME_REGEX.match(username) is not None
def password_pass_regex(password):
    return PASSWORD_REGEX.match(password) is not None


@cbv(router)
class UsersCBV:

    ''' CREATE '''
    @router.post("/user/register", status_code=status.HTTP_201_CREATED)
    def create(self, user: UserBM):

        if not user.username or not username_pass_regex(user.username):
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = {'message': 'Username must be at least 4 alphanumeric characters long & may contain . - _ chars.'}
            )
        if not user.password or not password_pass_regex(user.password):
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = {'Password must at least 6 chars and may contain . - _ symbols'}
            )

        passwd = user.password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashedpw = bcrypt.hashpw(passwd, salt).decode('utf-8')

        db_user = User(
            username = user.username,
            userhash = hashedpw
        )

        try:
            db_user.save()
        except mongoengine.errors.NotUniqueError:
            return JSONResponse(
                status_code = status.HTTP_409_CONFLICT,
                content = {'That user already exist'}
            )

        user = UserBM.parse_raw(db_user.to_json())

        log.info(f'User "{ user.username }" has been registered')

        return JSONResponse(
                status_code = status.HTTP_201_CREATED,
                content = {
                    'message': 'user registered',
                    'username': user.username,
                    'uuid': user.uuid
                }
            )


        # # db_user = User(username = user.username).save()
        # user = UserBM.parse_raw(db_user.to_json())


        # return user

    ''' READ '''
    @router.get("/user/{uuid}")
    def read(self, uuid: str):

        try:
            db_user = User.objects.get(uuid = uuid)
        except User.DoesNotExist:
            return JSONResponse(
                status_code = status.HTTP_404_NOT_FOUND,
                content = {'message': 'User does not found'}
            )

        user = UserBM.parse_raw(db_user.to_json())
        return user

    ''' UPDATE '''
    @router.put("/user/{uuid}")
    def update(self, uuid: str, user: UserBM):
        db_user = User.objects.get(uuid = uuid)
        db_user.username = user.username
        db_user.save()
        user = UserBM.parse_raw(db_user.to_json())
        return JSONResponse(
            status_code = status.HTTP_200_OK,
            content = {'message': 'Username updated',
                       'username': user.username
            }
        )

    ''' DELETE '''
    @router.delete("/user/{uuid}", status_code=status.HTTP_204_NO_CONTENT)
    def delete(self, uuid: str):

        db_user = User.objects.get(uuid = uuid)
        user = UserBM.parse_raw(db_user.to_json())
        db_user.delete()

        return JSONResponse(
            status_code = status.HTTP_204_NO_CONTENT,
            content = {'message': f'User "{user.username}" deleted'}
        )

        