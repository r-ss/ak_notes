from typing import Optional

from fastapi_utils.cbv import cbv
from fastapi import status, Depends
from fastapi_utils.inferring_router import InferringRouter

from models.user import UserTokenBM
from models.category import CategoryBM

from services.categories import CategoriesService
from services.users.auth import token_required

from pydantic import UUID4

router = InferringRouter(tags=['Categories'])


@cbv(router)
class CategoriesCBV:

    """ CREATE """
    @router.post('/categories', status_code=status.HTTP_201_CREATED)
    def category_create(self, category: CategoryBM, token: UserTokenBM = Depends(token_required)):
        return CategoriesService.create(category.name, token)

    """ READ """
    @router.get('/categories')
    def category_read_all(self, token: UserTokenBM = Depends(token_required), only_last: Optional[str] = None):
        if not only_last:
            return CategoriesService.read_all(token)
        return CategoriesService.get_last_one(token)

    @router.get('/categories/{uuid}')
    def category_read(self, uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        return CategoriesService.read_specific(uuid, token)    

    """ UPDATE """
    @router.put('/categories/{uuid}')
    def category_update(self, category: CategoryBM, token: UserTokenBM = Depends(token_required)):
        if not category.uuid:
            raise ValueError('uuid not given')
        return CategoriesService.update(category, token)

    """ DELETE """
    @router.delete('/categories/{uuid}', status_code=status.HTTP_204_NO_CONTENT)
    def category_delete(self, uuid: UUID4, token: UserTokenBM = Depends(token_required)):
        CategoriesService.delete(uuid, token)
        return {'category deleted'}
