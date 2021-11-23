from dao.dao import BasicDAOLayer
from models.user import UserBM
from models.category import Category, CategoryBM, CategoriesBM


class CategoryDAOLayer(BasicDAOLayer):

    def __init__(self):
        self.target = Category
        self.readable = 'Category'

    def get(self, response_model=CategoryBM, **kwargs):
        return super().get(response_model=response_model, **kwargs)

    def get_all(self):
        return super().get_all(response_model=CategoriesBM)

    def get_last_for_user(self, user: UserBM):
        return super().get(uuid=user.categories[-1], response_model=CategoryBM)

    def create(self, category: CategoryBM):
        return super().create(category, response_model=CategoryBM)

    def update_fields(self, fields: dict = {}, response_model=CategoryBM, **kwargs):
        return super().update_fields(fields=fields, response_model=response_model, **kwargs)

    def get_all_where(self, **kwargs):
        return super().get_all_where(response_model=CategoriesBM, **kwargs)
