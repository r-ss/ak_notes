from fastapi import status, HTTPException
from pydantic import UUID4

from models.category import Category, CategoryBM, CategoriesBM
from models.user import UserTokenBM

from services.users.auth import owner_or_admin_can_proceed_only
# from config import config

class CategoriesService:

    """ CREATE SERVICE """
    def create(name: str, token: UserTokenBM) -> CategoryBM:
        """ Create category item and return it """
        c = Category(
            name=name
        )
        c.save()
        return CategoryBM.from_orm(c)

    """ READ SERVICE """
    def read_specific(uuid: UUID4, token: UserTokenBM) -> CategoryBM:
        """ Get specific category item """

        try:
            db_category = Category.objects.get(uuid=uuid)
        except Category.DoesNotExist:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category does not found')

        # TODO - owner_or_admin_can_proceed_only(db_category.owner.uuid, token)

        return CategoryBM.from_orm(db_category)

        

    def read_all(token: UserTokenBM) -> CategoriesBM:
        """ Get all category items by current user """

        # TODO - filted by owner

        return CategoriesBM.from_orm(list(Category.objects.all()))

    """ UPDATE SERVICE """
    def update(category: CategoryBM, token: UserTokenBM) -> CategoryBM:
        """ Method to change category name """

        db_category = Category.objects.get(uuid=category.uuid)

        # TODO - owner_or_admin_can_proceed_only(db_category.owner.uuid, token)

        db_category.name = category.name
        return CategoryBM.from_orm(db_category.save())

    """ DELETE SERVICE """
    def delete(uuid: UUID4, token: UserTokenBM) -> None:
        """ Delete Category from database """

        db_category = Category.objects.get(uuid=uuid)
        db_category.delete()
