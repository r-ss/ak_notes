from typing import Union
from models.category import Category, CategoryBM


def create(name: str) -> Category:
    return Category(name=name).save()


def get_specific(numerical_id: int) -> Union[Category, None]:
    try:
        db_category = Category.objects.get(numerical_id=numerical_id)
    except Category.DoesNotExist:
        return None
    return db_category


def get_all() -> Category:
    return Category.objects.all()


def update(numerical_id: int, category: CategoryBM) -> Category:
    db_category = Category.objects.get(numerical_id=numerical_id)
    db_category.name = category.name
    return db_category.save()


def delete_category_from_db(numerical_id: int) -> None:
    db_category = Category.objects.get(numerical_id=numerical_id)
    db_category.delete()
