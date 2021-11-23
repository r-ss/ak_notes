from dao.dao import BasicDAOLayer
from pydantic import UUID4

from models.user import UserBM
from models.category import Category, CategoryBM, CategoriesBM


class CategoryDAOLayer(BasicDAOLayer):

    def __init__(self):
        self.target = Category
        self.readable = 'Category'

    def get(self, uuid: UUID4):
        return super().get(key=uuid, response_model=CategoryBM)

    def get_all(self):
        return super().get_all(response_model=CategoriesBM)

    def get_last_for_user(self, user: UserBM):
        return super().get(user.categories[-1], response_model=CategoryBM)

    def create(self, category: CategoryBM):
        return super().create(category, response_model=CategoryBM)

    def update_fields(self, uuid: UUID4, fields_dict: dict = {}):
        return super().update_fields(key=uuid, fields_dict=fields_dict, response_model=CategoryBM)

    def get_all_where(self, **kwargs):
        return super().get_all_where(response_model=CategoriesBM, **kwargs)
