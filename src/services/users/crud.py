from typing import Union
from fastapi import status, HTTPException

import mongoengine as mongoengine  # to catch mongoengine.errors.NotUniqueError on duplicate user registration

from models.user import User, UserBM, UserTokenBM, UserRegBM, UserTokenBM
# from config import Config

from services.users.auth import hash_password, owner_or_admin_can_proceed_only

from services.resslogger import RessLogger
log = RessLogger()

def create(user: UserRegBM) -> User:

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


def read(uuid: str) -> Union[User, None]:

    try:
        db_user = User.objects.get(uuid=uuid)
    except User.DoesNotExist:
        return None

    return db_user


def update(uuid: str, user: UserBM, token: UserTokenBM) -> User:
    db_user = User.objects.get(uuid=uuid)
    owner_or_admin_can_proceed_only(uuid, token)
    db_user.username = user.username
    return db_user.save()


def delete(uuid: str, token: UserTokenBM) -> None:

    db_user = User.objects.get(uuid=uuid)
    owner_or_admin_can_proceed_only(uuid, token)
    db_user.delete()
