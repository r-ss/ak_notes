from fastapi_utils.cbv import cbv
from fastapi import status, Depends
from fastapi.responses import JSONResponse
from fastapi_utils.inferring_router import InferringRouter

from models.user import UserTokenBM
from models.category import CategoryBM, CategoriesBM

from services.category import CategoryCRUD
from services.users.auth import token_required, owner_or_admin_can_proceed_only

router = InferringRouter(tags=['Categories'])


@cbv(router)
class CategoriesCBV:

    """ CREATE """
    @router.post('/categories', status_code=status.HTTP_201_CREATED)
    def category_create(self, category: CategoryBM, token: UserTokenBM = Depends(token_required)):
        db_category = CategoryCRUD.create(category.name)
        category = CategoryBM.parse_raw(db_category.to_json())
        return category

    """ READ """
    @router.get('/categories/{numerical_id}')
    def category_read(self, numerical_id: int, token: UserTokenBM = Depends(token_required)):
        db_category = CategoryCRUD.read_specific(numerical_id)

        if not db_category:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={'message': 'Category does not found'},
            )

        category = CategoryBM.parse_raw(db_category.to_json())
        return category

    @router.get('/categories')
    def category_read_all(self, token: UserTokenBM = Depends(token_required)):
        db_categories = CategoryCRUD.read_all()
        categories = CategoriesBM.parse_raw(db_categories.to_json())
        return categories

    """ UPDATE """
    @router.put('/categories/{numerical_id}')
    def category_update(self, numerical_id: int, category: CategoryBM, token: UserTokenBM = Depends(token_required)):
        db_category = CategoryCRUD.update(numerical_id, category)
        category = CategoryBM.parse_raw(db_category.to_json())
        return category

    """ DELETE """
    @router.delete('/categories/{numerical_id}', status_code=status.HTTP_204_NO_CONTENT)
    def category_delete(self, numerical_id: int, token: UserTokenBM = Depends(token_required)):
        db_category = CategoryCRUD.read_specific(numerical_id)
        category = CategoryBM.parse_raw(db_category.to_json())
        CategoryCRUD.delete(numerical_id)
        return {'deleted category': category}
