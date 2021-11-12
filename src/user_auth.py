import datetime
from fastapi_utils.cbv import cbv
from fastapi import status, Request, Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter
from re import compile

import bcrypt
import jwt

from config import Config

from models.user import User, UserTokenBM

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# from main import oauth2_scheme

# import mongoengine
# from mongoengine.queryset.visitor import Q as mongo_Q

from models.user import User

from resslogger import RessLogger
log = RessLogger()

USERNAME_REGEX = compile(r'\A[\w\-\.]{3,}\Z')
PASSWORD_REGEX = compile(r'\A[\w\-\.]{6,}\Z')

# checking username for valid characters
def username_pass_regex(username):
    return USERNAME_REGEX.match(username) is not None
def password_pass_regex(password):
    return PASSWORD_REGEX.match(password) is not None

def hash_password(pwd) -> str:
    pwd = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd, salt).decode('utf-8')

router = InferringRouter()



def owner_or_admin_can_proceed_only(uuid: str, token: UserTokenBM):
    if not token.is_superadmin and not str(uuid) == str(token.uuid):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Seems like you are not authorized to this')

    # if token.is_superadmin:
    #     return
    # else:
    #     db_user = User.objects.get(uuid = uuid)
    #     if db_user.username == token.username:
    #         return

    # raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Seems like you are not authorized to this')




async def token_required(token: str = Depends(oauth2_scheme)):
    dict = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
    token = UserTokenBM.parse_obj(dict)
    return token


@cbv(router)
class AuthCBV:

    ''' LOGIN '''
    @router.post('/token', status_code=status.HTTP_202_ACCEPTED)
    def login(self, form_data: OAuth2PasswordRequestForm = Depends()):

        if not form_data.password or not form_data.username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username and password must be provided for login')
        if not username_pass_regex(form_data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Username must be at least 3 characters and may contain . - _ chars.')
        if not password_pass_regex(form_data.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password must at least 6 characters and may contain . - _ symbols')

        

        try:
            db_user = User.objects.get(username = form_data.username)
            # user = User.objects.filter( mongo_Q(username = username) | mongo_Q(email = username) )[0] # useful to login by email as well by username
        except IndexError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")


        if bcrypt.checkpw(form_data.password.encode('utf-8'), db_user.userhash.encode('utf-8')):

            timeLimit = datetime.datetime.utcnow() + datetime.timedelta(days=30) # set token time limit
            payload = {
                'username': db_user.username,
                'uuid': str(db_user.uuid),
                'is_superadmin': db_user.is_superadmin,
                'expires': str(timeLimit)
            }
            # encrypt payload into token
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

            db_user.last_login = datetime.datetime.utcnow()
            db_user.save()

            log.info(f'User { db_user.username } logged in')

            return {'access_token': token, 'token_type': 'bearer'}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong password")


    ''' CHECK TOKEN '''
    @router.get("/check_token", status_code=status.HTTP_200_OK)
    def check_token(self, token: UserTokenBM = Depends(token_required)):
        return {'token': token}

    
    ''' SECRET PAGE, USED TO ENSURE TOKEN MECHANIC WORKING '''
    # @router.get("/secretpage", dependencies=[Depends(token_required)], status_code=status.HTTP_200_OK)
    @router.get("/secretpage", status_code=status.HTTP_200_OK)
    def secretpage(self, token: UserTokenBM = Depends(token_required)):
        return {'message': 'this is secret message'}


