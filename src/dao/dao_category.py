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

    #     """ Get all objects filtered by some rule """

        

        
    #     # print('*args', *args)
    #     for field, value in kwargs.items():
    #         # key = key.split('__')
    #         print(field)

    #         value = list(value)

    #         print("{0} = {1}".format(field, value))

    #         agg = []

    #         for item in value:
    #             print(str(item))
    #             agg.append(str(item))

            

    #         db_objs = self.target.objects(__raw__={'uuid': {'$in': agg}})

    #     print('db_objs', db_objs)


    #     if response_model:
    #         return response_model.from_orm(list(db_objs))
    #     return db_objs


    # def update_fields(self, uuid: UUID4, field='uuid', fields_dict={}):
    #     return super().update_fields(uuid, field=field, fields_dict=fields_dict)



    # def delete(self, uuid: UUID4):
    #     return super().delete(uuid)

    # def update_fields(self, uuid: UUID4, field='uuid', fields_dict={}, response_model=CategoryBM):

    #     db_obj = super().get(key=uuid)

    #     for k, v in fields_dict.items():
    #         db_obj[k] = v
    #     db_obj.save()

    #     if response_model:
    #         return response_model.from_orm(db_obj)
    #     return db_obj