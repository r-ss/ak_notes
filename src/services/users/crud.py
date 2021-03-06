from fastapi import status, HTTPException
from pydantic import UUID4

from models.user import UserBM, UsersBM, UserTokenBM, UserRegBM

from dao.dao_user import UserDAOLayer

from services.users.auth import Auth
from services.categories import CategoriesService

from services.resslogger import RessLogger

log = RessLogger()
UserDAO = UserDAOLayer()


class UsersService:

    """CREATE SERVICE"""

    def create(user: UserRegBM) -> UserBM:
        """Create user in database and return it"""

        user.userhash = Auth.hash_password(user.password.get_secret_value())

        user = UserDAO.create(user)

        log.info(f'User "{ user.username }" has been registered')
        # create default Category for new User
        CategoriesService.create_default(user)

        return user

    """ READ SERVICE """

    def read_all() -> UsersBM:
        """Get all users from database and return them"""
        return UserDAO.get_all()

    def read_specific(uuid: UUID4) -> UserBM:
        """Get specific user from database and return"""
        return UserDAO.get(uuid=uuid)

    """ UPDATE SERVICE """

    def edit_username(input_user: UserBM, token: UserTokenBM) -> UserBM:
        """Change username of specific user in database and returu User with updated data"""

        user = UserDAO.get(uuid=input_user.uuid)

        if user.uuid != token.uuid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not allowed")

        user.username = input_user.username
        return UserDAO.update_fields(uuid=user.uuid, fields={"username": user.username})

    """ DELETE SERVICE """

    def delete(uuid: UUID4, token: UserTokenBM) -> None:
        """Delete user from database"""

        user = UserDAO.get(uuid=uuid)

        if user.uuid != token.uuid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not allowed")

        # Delete all users categories
        for cat_uuid in user.categories:
            CategoriesService.delete(cat_uuid, token, already_authenticated_user=user)

        UserDAO.delete(uuid=user.uuid)
