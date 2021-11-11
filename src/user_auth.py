import datetime
from fastapi_utils.cbv import cbv
from fastapi import status, Request, Depends, Header, HTTPException
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter
from re import compile

import bcrypt
import jwt

from config import Config

from models.user import UserRegBM, UserTokenBM, UserTokenDataBM

# import mongoengine
# from mongoengine.queryset.visitor import Q as mongo_Q

from models.user import User

from resslogger import RessLogger
log = RessLogger()

USERNAME_REGEX = compile(r'\A[\w\-\.]{4,}\Z')
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


# async def token_required(request: Request, token: str = Header(...)):
async def token_required(request: Request, x_token: str = Header(...)):

    try:
        if 'X-Token' in request.headers:
            token = request.headers['X-Token']
        else:
            token = request.headers['Authorization']
    except:
        try:
            token = await request.json()['X-Token']
        except:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "token required")
            # return JSONResponse(status_code = status.HTTP_401_UNAUTHORIZED, content = {'message': 'token required'})

    if token:
        try:
            tokendata = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])               
        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "token has expired")
            # return JSONResponse(status_code = status.HTTP_401_UNAUTHORIZED, content = {'message': 'token has expired'})
        except jwt.exceptions.InvalidTokenError:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "invalid token")
            # return JSONResponse(status_code = status.HTTP_401_UNAUTHORIZED, content = {'message': 'invalid token'})

        return 

    else:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = "token required")
        # return JSONResponse(status_code = status.HTTP_401_UNAUTHORIZED, content = {'message': 'token required'})



@cbv(router)
class AuthCBV:

    ''' LOGIN '''
    @router.post("/login", status_code=status.HTTP_202_ACCEPTED)
    def login(self, user: UserRegBM):

        if not user.password or not user.username:
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = {'message': 'Username and password must be provided for login'}
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

        try:
            db_user = User.objects.get(username = user.username)
            # user = User.objects.filter( mongo_Q(username = username) | mongo_Q(email = username) )[0] # useful to login by email as well by username
        except IndexError:
            return JSONResponse(
                status_code = status.HTTP_400_BAD_REQUEST,
                content = {'message': 'User not found'}
            )

        if bcrypt.checkpw(user.password.encode('utf-8'), db_user.userhash.encode('utf-8')):

            timeLimit = datetime.datetime.utcnow() + datetime.timedelta(days=30) # set token time limit
            payload = {
                'username': db_user.username,
                'uuid': str(db_user.uuid),
                'is_superadmin': db_user.is_superadmin,
                'exp': timeLimit
            }
            # encrypt payload into token
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

            db_user.last_login = datetime.datetime.utcnow()
            db_user.save()

            log.info(f'User { db_user.username } logged in')

            return {
                'auth': True,
                'token': token, # token.decode('utf-8')
                'user': db_user.to_json(),
                'token_expires_at': f'{timeLimit}'
            }
        else:
            return JSONResponse(
                status_code = status.HTTP_401_UNAUTHORIZED,
                content = {'auth': False, 'message': 'Wrong password'}
            )

    ''' CHECK TOKEN '''
    @router.post("/token", status_code=status.HTTP_202_ACCEPTED)
    def check_token(self, token: UserTokenBM):
        try:
            decoded_data = jwt.decode(token.token, Config.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            return JSONResponse(
                status_code = status.HTTP_401_UNAUTHORIZED,
                content = {'auth': False, 'message': 'Token has expired'}
            )
        except:
            return JSONResponse(
                status_code = status.HTTP_401_UNAUTHORIZED,
                content = {'auth': False, 'message': 'Invalid Token'}
            )

        return {
            'resource': 'token',
            'username': decoded_data['username'],
            'uuid': decoded_data['uuid'],
            'expires': datetime.datetime.fromtimestamp(decoded_data['exp']).strftime(Config.DATETIME_FORMAT_HUMAN),
        }

    
    ''' SECRET PAGE, USED TO ENSURE TOKEN MECHANIC WORKING '''
    @router.get("/secretpage", dependencies=[Depends(token_required)], status_code=status.HTTP_200_OK)
    def secretpage(self):
        return {'message': 'this is secret message'}


