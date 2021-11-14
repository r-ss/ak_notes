from fastapi_utils.cbv import cbv
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from models.category import CategoryBM, CategoriesBM

from services.category_logic import create, get_specific, get_all, update, delete_category_from_db

router = InferringRouter()


@cbv(router)
class CategoriesCBV:

    """ CREATE """
    @router.post('/categories', status_code=status.HTTP_201_CREATED)
    def category_create(self, category: CategoryBM):
        db_category = create(category.name)
        category = CategoryBM.parse_raw(db_category.to_json())
        return category

    """ READ """
    @router.get('/categories/{numerical_id}')
    def category_read(self, numerical_id: int):
        db_category = get_specific(numerical_id)

        if not db_category:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={'message': 'Category does not found'},
            )

        category = CategoryBM.parse_raw(db_category.to_json())
        return category

    @router.get('/categories')
    def category_read_all(self):
        db_categories = get_all()
        categories = CategoriesBM.parse_raw(db_categories.to_json())
        return categories

    """ UPDATE """
    @router.put('/categories/{numerical_id}')
    def category_update(self, numerical_id: int, category: CategoryBM):
        db_category = update(numerical_id, category)
        category = CategoryBM.parse_raw(db_category.to_json())
        return category

    """ DELETE """
    @router.delete('/categories/{numerical_id}', status_code=status.HTTP_204_NO_CONTENT)
    def category_delete(self, numerical_id: int):
        db_category = get_specific(numerical_id)
        category = CategoryBM.parse_raw(db_category.to_json())
        delete_category_from_db(numerical_id)
        return {'deleted category': category}
