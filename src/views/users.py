from fastapi_utils.cbv import cbv
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

# Following mongoengine import needed here just once for catch
# exception mongoengine.errors.NotUniqueError upon duplicate user reg
import mongoengine as mongoengine


from re import compile


from models.user import User, UserBM, UserRegBM

from user_auth import hash_password, username_pass_regex, password_pass_regex

router = InferringRouter()

from resslogger import RessLogger
log = RessLogger()

@cbv(router)
class UsersCBV:

    ''' CREATE '''
    @router.post("/user/register", status_code=status.HTTP_201_CREATED)
    def create(self, user: UserRegBM):

        if not user.password or not user.username:
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = {'message': 'Username and password must be provided for registration'}
            )

        if not username_pass_regex(user.username):
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = {'message': 'Username must be at least 4 characters and may contain . - _ chars.'}
            )
        if not password_pass_regex(user.password):
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = {'message': 'Password must at least 6 characters and may contain . - _ symbols'}
            )


        db_user = User(
            username = user.username,
            userhash = hash_password(user.password)
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

        