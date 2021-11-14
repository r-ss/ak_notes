import datetime
import bcrypt
import jwt
from re import compile
from fastapi_utils.cbv import cbv
from fastapi import status, Depends, HTTPException
from fastapi_utils.inferring_router import InferringRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.user import User, UserTokenBM
from config import Config

from resslogger import RessLogger
log = RessLogger()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

router = InferringRouter()


def username_pass_regex(username) -> bool:
    regex = compile(Config.AUTH_USERNAME['regex'])
    return regex.match(username) is not None


def password_pass_regex(password) -> bool:
    regex = compile(Config.AUTH_PASSWORD['regex'])
    return regex.match(password) is not None


def hash_password(pwd) -> str:
    """ Application-wide method to get hash from a password
        Used upon registration and login
    """
    pwd = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(pwd, salt).decode('utf-8')


def owner_or_admin_can_proceed_only(uuid: str, token: UserTokenBM) -> None:
    """ Compare uuid of object with uuid of current user 
        Throw an HTTPException if current user is not own object
        Method can be invoked in a middle of views to stop unauthorized operations
    """
    if not token.is_superadmin and not str(uuid) == str(token.uuid):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Seems like you are not authorized to this',
        )


async def token_required(token: str = Depends(oauth2_scheme)) -> UserTokenBM:
    """ Decode user token from header. Used in views that requires authentication
        Example in FastAPI Docs:
        https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    """
    dict = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.AUTH_HASHING_ALGORITHM])
    token = UserTokenBM.parse_obj(dict)
    return token


@cbv(router)
class AuthCBV:

    """ LOGIN """
    @router.post('/token', status_code=status.HTTP_202_ACCEPTED)
    def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        def bad_req(msg: str):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

        if not form_data.password or not form_data.username:
            bad_req('Username and password must be provided for login')
        if not username_pass_regex(form_data.username):
            bad_req(Config.AUTH_USERNAME['failmessage'])
        if not password_pass_regex(form_data.password):
            bad_req(Config.AUTH_PASSWORD['failmessage'])

        try:
            db_user = User.objects.get(username=form_data.username)
            """ If in future we want login not just by username but username OR email,
                we can use something like that:
                db_user = User.objects.filter( mongo_Q(username = username) | mongo_Q(email = username) )[0]
            """
        except IndexError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')


        # If password correct login and return token to client
        if bcrypt.checkpw(form_data.password.encode('utf-8'), db_user.userhash.encode('utf-8')):

            timeLimit = datetime.datetime.utcnow() + datetime.timedelta(days=30)  # set token time limit
            payload = {
                'username': db_user.username,
                'uuid': str(db_user.uuid),
                'is_superadmin': db_user.is_superadmin,
                'expires': str(timeLimit),
            }
            token = jwt.encode(payload, Config.SECRET_KEY, algorithm=Config.AUTH_HASHING_ALGORITHM)  # encrypt payload into token

            db_user.last_login = datetime.datetime.utcnow()
            db_user.save()

            log.info(f'User { db_user.username } logged in')

            return {'access_token': token, 'token_type': 'bearer'}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong password')

    """ CHECK TOKEN """
    @router.get('/check_token', status_code=status.HTTP_200_OK)
    def check_token(self, token: UserTokenBM = Depends(token_required)):
        return {'token': token}

    """ SECRET PAGE, USED TO ENSURE TOKEN MECHANIC WORKING """
    @router.get('/secretpage', status_code=status.HTTP_200_OK)
    def secretpage(self, token: UserTokenBM = Depends(token_required)):
        return {'message': 'this is secret message'}
