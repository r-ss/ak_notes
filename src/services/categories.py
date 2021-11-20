from fastapi import status, HTTPException
from pydantic import UUID4

from models.category import Category, CategoryBM, CategoriesBM
from models.user import User, UserTokenBM

# from services.users.auth import owner_or_admin_can_proceed_only
# from config import config


class CategoriesService:

    def get_user_helper(token: UserTokenBM, already_authenticated_user=None) -> User:
        """ To reduce code repeat """
        db_user = already_authenticated_user
        if not already_authenticated_user:
            try:
                db_user = User.objects.get(uuid=token.uuid)
            except User.DoesNotExist:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User does not found')
        return db_user

    """ CREATE SERVICE """
    def create(name: str, token: UserTokenBM) -> CategoryBM:
        """ Create category item and return it """

        db_user = CategoriesService.get_user_helper(token)

        c = Category(name=name).save()

        db_user.categories.append(c.uuid)
        db_user.save()

        return CategoryBM.from_orm(c)

    def create_default(db_user: User) -> None:
        """ Create default category for just registered user """
        c = Category(name=f'Default for {db_user.username}').save()
        db_user.categories.append(str(c.uuid))
        db_user.save()

    """ READ SERVICE """
    def read_specific(uuid: UUID4, token: UserTokenBM) -> CategoryBM:
        """ Get specific category item """

        # db_user = CategoriesService.get_user_helper(token)

        try:
            db_category = Category.objects.get(uuid=uuid)
        except Category.DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category does not found')

        # TODO - owner_or_admin_can_proceed_only(db_category.owner.uuid, token)

        return CategoryBM.from_orm(db_category)

    def read_all(token: UserTokenBM) -> CategoriesBM:
        """ Get all category items by current user """

        db_user = CategoriesService.get_user_helper(token)
        categories = db_user.categories

        return CategoriesBM.from_orm(list(Category.objects(uuid__in=categories)))

    def get_last_one(token: UserTokenBM) -> CategoryBM:
        db_user = CategoriesService.get_user_helper(token)
        # db_category = Category.objects.get(uuid=db_user.categories[-1])
        return CategoryBM.from_orm(Category.get_last_for_user(db_user))

    """ UPDATE SERVICE """
    def update(category: CategoryBM, token: UserTokenBM) -> CategoryBM:
        """ Method to change category name """

        # db_user = CategoriesService.get_user_helper(token)
        db_category = Category.objects.get(uuid=category.uuid)

        # TODO - owner_or_admin_can_proceed_only(db_category.owner.uuid, token)

        db_category.name = category.name
        return CategoryBM.from_orm(db_category.save())

    """ DELETE SERVICE """
    def delete(uuid: UUID4, token: UserTokenBM, already_authenticated_user=None) -> None:
        """ Delete Category from database """

        db_user = CategoriesService.get_user_helper(token, already_authenticated_user)

        # TODO - owner_or_admin_can_proceed_only(db_category.owner.uuid, token)

        db_category = Category.objects.get(uuid=uuid)
        db_category.delete()

        db_user.categories.remove(db_category.uuid)
        db_user.save()
