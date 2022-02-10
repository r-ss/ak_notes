import datetime
import bcrypt
import jwt
from re import compile
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from pydantic import UUID4

from dao.dao_user import UserDAOLayer
from models.user import UserBM, UserTokenBM
from config import config

from services.resslogger import RessLogger

log = RessLogger()

UserDAO = UserDAOLayer()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def token_required(token: str = Depends(oauth2_scheme)) -> UserTokenBM:
    """Decode user token from header. Used in views that requires authentication
    Example in FastAPI Docs:
    https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
    """
    dict = jwt.decode(token, config.SECRET_KEY, algorithms=[config.AUTH_HASHING_ALGORITHM])
    token = UserTokenBM.parse_obj(dict)
    return token


def check_ownership(uuid: UUID4, token: UserTokenBM) -> None:
    """Compare uuid of object with uuid of current user
    Throw an HTTPException if current user is not own object
    Method can be invoked in a middle of views to stop unauthorized operations
    """
    if not token.is_superadmin and not str(uuid) == str(token.uuid):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Seems like you are not authorized to this",
        )


class Auth:
    def is_username_valid(username) -> bool:
        """Username validation"""
        regex = compile(config.AUTH_USERNAME_REGEX["regex"])
        return regex.match(username) is not None

    def is_password_valid(password) -> bool:
        """Password validation"""
        regex = compile(config.AUTH_PASSWORD_REGEX["regex"])
        return regex.match(password) is not None

    def hash_password(pwd) -> str:
        """Application-wide method to get hash from a password
        Used upon registration and login
        """
        pwd = pwd.encode("utf-8")
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(pwd, salt).decode("utf-8")

    def encode_access_token(user: UserBM):

        payload = {
            "exp": datetime.datetime.utcnow() + config.AUTH_ACCESS_TOKEN_EXPIRATION_TIME,  # set access token time limit
            "iat": datetime.datetime.utcnow(),  # issued at
            "scope": "access_token",
            "username": user.username,
            "uuid": str(user.uuid),
            "is_superadmin": user.is_superadmin,
        }

        return jwt.encode(payload, config.SECRET_KEY, algorithm=config.AUTH_HASHING_ALGORITHM)  # encrypt payload into token

    def encode_refresh_token(user: UserBM):

        payload = {
            "exp": datetime.datetime.utcnow() + config.AUTH_REFRESH_TOKEN_EXPIRATION_TIME,  # set refresh token time limit
            "iat": datetime.datetime.utcnow(),  # issued at
            "scope": "refresh_token",
            "username": user.username,
            "uuid": str(user.uuid),
            "is_superadmin": user.is_superadmin,
        }

        return jwt.encode(payload, config.SECRET_KEY, algorithm=config.AUTH_HASHING_ALGORITHM)  # encrypt payload into token

    def check_refresh_token(refresh_token):
        try:
            dict = jwt.decode(refresh_token, config.SECRET_KEY, algorithms=[config.AUTH_HASHING_ALGORITHM])
            if dict["scope"] == "refresh_token":

                user = UserDAO.get(uuid=dict["uuid"])

                new_access_token = Auth.encode_access_token(user)
                new_refresh_token = Auth.encode_refresh_token(user)

                return new_access_token, new_refresh_token

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid scope for token")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    def login(username: str, password: str) -> bool:

        db_user = UserDAO.get(username=username, response_model=None)

        # If password correct login and return token to client
        if bcrypt.checkpw(password.encode("utf-8"), db_user.userhash.encode("utf-8")):

            user = UserBM.from_orm(db_user)

            access_token = Auth.encode_access_token(user)
            refresh_token = Auth.encode_refresh_token(user)

            UserDAO.update_fields(uuid=user.uuid, fields={"last_login": datetime.datetime.utcnow()})

            log.info(f"User { user.username } logged in")

            return user, access_token, refresh_token
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Wrong password")
