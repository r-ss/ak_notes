from typing import Union
from fastapi import status, HTTPException

import mongoengine as mongoengine  # to catch mongoengine.errors.NotUniqueError on duplicate user registration

from models.user import User, UserBM, UserTokenBM, UserRegBM, UserTokenBM

# from config import config

from services.users.auth import hash_password, owner_or_admin_can_proceed_only
from services.categories import CategoriesService

from services.resslogger import RessLogger

log = RessLogger()


class UsersService:

    """ CREATE SERVICE """
    def create(user: UserRegBM) -> UserBM:
        """ Create user in database and return it """

        db_user = User(username=user.username, userhash=hash_password(user.password))

        try:
            db_user.save()
        except mongoengine.errors.NotUniqueError:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='That user already exist')

        log.info(f'User "{ db_user.username }" has been registered')


        # create default Category for new User
        CategoriesService.create_default(db_user)



        return UserBM.from_orm(db_user)

    """ READ SERVICE """
    def read(uuid: str) -> UserBM:
        """ Get specific user from database and return. Return None if not found in db """

        try:
            db_user = User.objects.get(uuid=uuid)
        except User.DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not found')

        return UserBM.from_orm(db_user)

    """ UPDATE SERVICE """
    def update(user: UserBM, token: UserTokenBM) -> UserBM:
        """ Change username of specific user in database and returu User with updated data """

        db_user = User.objects.get(uuid=user.uuid)

        owner_or_admin_can_proceed_only(db_user.uuid, token)

        db_user.username = user.username
        return UserBM.from_orm(db_user.save())

    """ DELETE SERVICE """
    def delete(uuid: str, token: UserTokenBM) -> None:
        """ Delete user from database """

        db_user = User.objects.get(uuid=uuid)
        owner_or_admin_can_proceed_only(uuid, token)

        # Delete all users categories
        for cat_uuid in db_user.categories:
            CategoriesService.delete(cat_uuid, token, already_authenticated_user = db_user)


        db_user.delete()
