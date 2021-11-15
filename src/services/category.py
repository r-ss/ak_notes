from typing import Union
from models.category import Category, CategoryBM


class CategoryCRUD:

    """ CREATE SERVICE """
    def create(name: str) -> Category:
        """ Create category item in database and return it """

        return Category(name=name).save()

    """ READ SERVICE """
    def read_specific(numerical_id: int) -> Union[Category, None]:
        """ Get specific category item from database and return it """

        try:
            db_category = Category.objects.get(numerical_id=numerical_id)
        except Category.DoesNotExist:
            return None
        return db_category

    def read_all() -> Category:
        """ Get all category items from database and return them """

        return Category.objects.all()

    """ UPDATE SERVICE """
    def update(numerical_id: int, category: CategoryBM) -> Category:
        """ Method to change category name """

        db_category = Category.objects.get(numerical_id=numerical_id)
        db_category.name = category.name
        return db_category.save()

    """ DELETE SERVICE """
    def delete(numerical_id: int) -> None:
        """ Delete Category from database """

        db_category = Category.objects.get(numerical_id=numerical_id)
        db_category.delete()
