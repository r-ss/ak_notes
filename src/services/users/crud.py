from typing import Union
from fastapi import status, HTTPException

import mongoengine as mongoengine  # to catch mongoengine.errors.NotUniqueError on duplicate user registration

from models.user import User, UserBM, UserTokenBM, UserRegBM, UserTokenBM

# from config import Config

from services.users.auth import hash_password, owner_or_admin_can_proceed_only

from services.resslogger import RessLogger

log = RessLogger()


class UsersCRUD:

    """ CREATE SERVICE """
    def create(user: UserRegBM) -> User:
        """ Create user in database and return it """

        db_user = User(username=user.username, userhash=hash_password(user.password))

        try:
            db_user.save()
        except mongoengine.errors.NotUniqueError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail='That user already exist',
            )

        log.info(f'User "{ db_user.username }" has been registered')
        return db_user

    """ READ SERVICE """
    def read(uuid: str) -> Union[User, None]:
        """ Get specific user from database and return. Return None if not found in db """

        try:
            db_user = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            return None

        return db_user

    """ UPDATE SERVICE """
    def update(uuid: str, user: UserBM, token: UserTokenBM) -> User:
        """ Change username of specific user in database and returu User with updated data """

        db_user = User.objects.get(uuid=uuid)
        owner_or_admin_can_proceed_only(uuid, token)
        db_user.username = user.username
        return db_user.save()

    """ DELETE SERVICE """
    def delete(uuid: str, token: UserTokenBM) -> None:
        """ Delete user from database """

        db_user = User.objects.get(uuid=uuid)
        owner_or_admin_can_proceed_only(uuid, token)
        db_user.delete()
