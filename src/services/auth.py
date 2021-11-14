from typing import Union
import datetime
import bcrypt
import jwt
from re import compile
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

import mongoengine as mongoengine  # to catch mongoengine.errors.NotUniqueError on duplicate user registration

from models.user import User, UserBM, UserTokenBM, UserRegBM, UserTokenBM
from config import Config

from services.resslogger import RessLogger
log = RessLogger()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def is_username_correct(username) -> bool:
    """ Username validation """
    regex = compile(Config.AUTH_USERNAME_REGEX['regex'])
    return regex.match(username) is not None


def is_password_correct(password) -> bool:
    """ Password validation """
    regex = compile(Config.AUTH_PASSWORD_REGEX['regex'])
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


def login(username: str, password: str) -> bool:

    try:
        db_user = User.objects.get(username=username)
        """ If in future we want login not just by username but username OR email,
            we can use something like that:
            db_user = User.objects.filter( mongo_Q(username = username) | mongo_Q(email = username) )[0]
        """
    except IndexError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')

    # If password correct login and return token to client
    if bcrypt.checkpw(password.encode('utf-8'), db_user.userhash.encode('utf-8')):

        timeLimit = datetime.datetime.utcnow() + Config.AUTH_TOKEN_EXPIRATION_TIME  # set token time limit
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

        return token
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Wrong password')


""" CRUD methods """


def create_user(user: UserRegBM) -> User:

    db_user = User(username=user.username, userhash=hash_password(user.password))

    try:
        db_user.save()
    except mongoengine.errors.NotUniqueError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='That user already exist',
        )

    log.info(f'User "{ db_user.username }" has been registered')
    return db_user


def get_user(uuid: str) -> Union[User, None]:

    try:
        db_user = User.objects.get(uuid=uuid)
    except User.DoesNotExist:
        return None

    return db_user


def update_user(uuid: str, user: UserBM, token: UserTokenBM) -> User:
    db_user = User.objects.get(uuid=uuid)
    owner_or_admin_can_proceed_only(uuid, token)
    db_user.username = user.username
    return db_user.save()


def delete_user(uuid: str, token: UserTokenBM) -> None:

    db_user = User.objects.get(uuid=uuid)
    owner_or_admin_can_proceed_only(uuid, token)
    db_user.delete()
