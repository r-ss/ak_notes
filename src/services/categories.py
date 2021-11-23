from pydantic import UUID4

from models.category import CategoryBM, CategoriesBM
from models.user import UserBM, UserTokenBM

from dao.dao_user import UserDAOLayer
from dao.dao_category import CategoryDAOLayer

UserDAO = UserDAOLayer()
CategoryDAO = CategoryDAOLayer()

# from services.users.auth import check_ownership
# from config import config


class CategoriesService:

    def get_user_helper(token: UserTokenBM, already_authenticated_user=None) -> UserBM:
        """ To reduce code repeat """
        if not already_authenticated_user:
            return UserDAO.get(uuid=token.uuid)
        return already_authenticated_user

    """ CREATE SERVICE """
    def create(name: str, token: UserTokenBM) -> CategoryBM:
        """ Create category item and return it """

        user = UserDAO.get(uuid=token.uuid)

        category = CategoryDAO.create(
            CategoryBM.parse_obj({'name': name})
        )

        user.categories.append(category.uuid)
        UserDAO.update_fields(uuid=user.uuid, fields={'categories': user.categories})
        return category

    def create_default(user: UserBM) -> None:
        """ Create default category for just registered user """

        category = CategoryDAO.create(
            CategoryBM.parse_obj({'name': f'Default for {user.username}'})
        )

        user.categories.append(category.uuid)
        UserDAO.update_fields(uuid=user.uuid, fields={'categories': user.categories})
        return category

    """ READ SERVICE """
    def read_specific(uuid: UUID4, token: UserTokenBM) -> CategoryBM:
        """ Get specific category item """
        # TODO - check_ownership(db_category.owner.uuid, token)
        return CategoryDAO.get(uuid=uuid)

    def read_all(token: UserTokenBM) -> CategoriesBM:
        """ Get all category items by current user """

        user = CategoriesService.get_user_helper(token)
        categories = user.categories

        return CategoryDAO.get_all_where(uuid__in=categories)

    def get_last_one(token: UserTokenBM) -> CategoryBM:
        user = CategoriesService.get_user_helper(token)
        # db_category = Category.objects.get(uuid=db_user.categories[-1])
        return CategoryDAO.get_last_for_user(user)

    """ UPDATE SERVICE """
    def update(input_category: CategoryBM, token: UserTokenBM) -> CategoryBM:
        """ Method to change category name """

        category = CategoryDAO.get(uuid=input_category.uuid)

        # TODO - check_ownership(db_category.owner.uuid, token)
        return CategoryDAO.update_fields(uuid=category.uuid, fields={'name': input_category.name})

    """ DELETE SERVICE """
    def delete(uuid: UUID4, token: UserTokenBM, already_authenticated_user=None) -> None:
        """ Delete Category from database """

        user = CategoriesService.get_user_helper(token, already_authenticated_user)

        # TODO - check_ownership(db_category.owner.uuid, token)
        category = CategoryDAO.get(uuid=uuid)
        CategoryDAO.delete(uuid=uuid)

        user.categories.remove(category.uuid)
        UserDAO.update_fields(uuid=user.uuid, fields={'categories': user.categories})
